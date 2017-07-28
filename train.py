from dialgarithm.dialgarithm import *
import numpy as np
import sklearn.gaussian_process as gp
from scipy.stats import norm
from scipy.optimize import minimize


class Bayes:
    @staticmethod
    def run_parameter_set(population_size, matches, starting_mutation_rate, mutation_delta):
        print("Running parameter set")
        try:
            Model.set_hyperparameters(population_size, matches, starting_mutation_rate, mutation_delta)
        except ValueError:
            return 0
        if Model.num_generations <= 0:
            print("Trivial zero")
            return 0
        else:
            print("Nontrivial")
            print(population_size, matches, starting_mutation_rate, mutation_delta)

        def run_attempt():
            print("Running attempt")
            evolve()
            output()
            return Evolve.get_best()

        attempts = sorted([run_attempt() for _ in range(0, 1)])
        return attempts[0]

    """
    Bayesian optimisation of loss functions.
    All credit below to Thomas Huijskens -- this code is taken from the following repo:
    https://github.com/thuijskens/bayesian-optimization/blob/master/python/gp.py
    """

    @staticmethod
    def expected_improvement(x, gaussian_process, evaluated_loss, greater_is_better=True, n_params=1):
        """ expected_improvement
        Expected improvement acquisition function.
        Arguments:
        ----------
            x: array-like, shape = [n_samples, n_hyperparams]
                The point for which the expected improvement needs to be computed.
            gaussian_process: GaussianProcessRegressor object.
                Gaussian process trained on previously evaluated hyperparameters.
            evaluated_loss: Numpy array.
                Numpy array that contains the values off the loss function for the previously
                evaluated hyperparameters.
            greater_is_better: Boolean.
                Boolean flag that indicates whether the loss function is to be maximised or minimised.
            n_params: int.
                Dimension of the hyperparameter space.
        """

        x_to_predict = x.reshape(-1, n_params)

        mu, sigma = gaussian_process.predict(x_to_predict, return_std=True)

        if greater_is_better:
            loss_optimum = np.max(evaluated_loss)
        else:
            loss_optimum = np.min(evaluated_loss)

        scaling_factor = (-1) ** (not greater_is_better)

        # In case sigma equals zero
        with np.errstate(divide='ignore'):
            Z = scaling_factor * (mu - loss_optimum) / sigma
            expected_improvement = scaling_factor * (mu - loss_optimum) * norm.cdf(Z) + sigma * norm.pdf(Z)
            expected_improvement[sigma == 0.0] = 0.0

        return -1 * expected_improvement

    @staticmethod
    def sample_next_hyperparameter(acquisition_func, gaussian_process, evaluated_loss, greater_is_better=False,
                                   bounds=(0, 10), n_restarts=25):
        """ sample_next_hyperparameter
        Proposes the next hyperparameter to sample the loss function for.
        Arguments:
        ----------
            acquisition_func: function.
                Acquisition function to optimise.
            gaussian_process: GaussianProcessRegressor object.
                Gaussian process trained on previously evaluated hyperparameters.
            evaluated_loss: array-like, shape = [n_obs,]
                Numpy array that contains the values off the loss function for the previously
                evaluated hyperparameters.
            greater_is_better: Boolean.
                Boolean flag that indicates whether the loss function is to be maximised or minimised.
            bounds: Tuple.
                Bounds for the L-BFGS optimiser.
            n_restarts: integer.
                Number of times to run the minimiser with different starting points.
        """
        print(bounds)
        best_x = None
        best_acquisition_value = 1
        n_params = bounds.shape[0]
        param_array = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_restarts, n_params))
        for starting_point in list(param_array):

            res = minimize(fun=acquisition_func,
                           x0=starting_point.reshape(1, -1),
                           bounds=bounds,
                           method='L-BFGS-B',
                           args=(gaussian_process, evaluated_loss, greater_is_better, n_params))

            if res.fun < best_acquisition_value:
                best_acquisition_value = res.fun
                best_x = res.x

        return best_x

    @staticmethod
    def bayesian_optimisation(n_iters, sample_loss, bounds, x0=None, n_pre_samples=5,
                              gp_params=None, random_search=False, alpha=1e-5, epsilon=1e-7):
        """ bayesian_optimisation
        Uses Gaussian Processes to optimise the loss function `sample_loss`.
        Arguments:
        ----------
            n_iters: integer.
                Number of iterations to run the search algorithm.
            sample_loss: function.
                Function to be optimised.
            bounds: array-like, shape = [n_params, 2].
                Lower and upper bounds on the parameters of the function `sample_loss`.
            x0: array-like, shape = [n_pre_samples, n_params].
                Array of initial points to sample the loss function for. If None, randomly
                samples from the loss function.
            n_pre_samples: integer.
                If x0 is None, samples `n_pre_samples` initial points from the loss function.
            gp_params: dictionary.
                Dictionary of parameters to pass on to the underlying Gaussian Process.
            random_search: integer.
                Flag that indicates whether to perform random search or L-BFGS-B optimisation
                over the acquisition function.
            alpha: double.
                Variance of the error term of the GP.
            epsilon: double.
                Precision tolerance for floats.
        """

        tentative_training = Writer.load_pickled_object('train.txt')
        if tentative_training is None:
            x_list = []
            y_list = []

            n_params = bounds.shape[0]

            if x0 is None:
                params_array = np.random.uniform(bounds[:, 0], bounds[:, 1], (n_pre_samples, bounds.shape[0]))
                for params in list(params_array):
                    x_list.append(params)
                    y_list.append(sample_loss(*params))
            else:
                for params in x0:
                    x_list.append(params)
                    y_list.append(sample_loss(params))

            xp = np.array(x_list)
            yp = np.array(y_list)
        else:
            xp, yp = tentative_training
            x_list = xp.tolist()
            y_list = yp.tolist()

        # Create the GP
        if gp_params is not None:
            model = gp.GaussianProcessRegressor(**gp_params)
        else:
            kernel = gp.kernels.Matern()
            model = gp.GaussianProcessRegressor(kernel=kernel,
                                                alpha=alpha,
                                                n_restarts_optimizer=10,
                                                normalize_y=True)

        iterations = 0
        while iterations < n_iters:

            model.fit(xp, yp)

            # Sample next hyperparameter
            if random_search:
                x_random = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(random_search, n_params))
                ei = -1 * Bayes.expected_improvement(x_random, model, yp, greater_is_better=True, n_params=n_params)
                next_sample = x_random[np.argmax(ei), :]
            else:
                next_sample = Bayes.sample_next_hyperparameter(Bayes.expected_improvement, model, yp,
                                                               greater_is_better=True, bounds=bounds, n_restarts=100)

            print(x_list)
            shifted_x_list = np.abs(x_list - xp)
            # Duplicates will break the GP. In case of a duplicate, we will randomly sample a next query point.
            if np.any(shifted_x_list):
                next_sample = np.random.uniform(bounds[:, 0], bounds[:, 1], bounds.shape[0])

            # Sample loss for new set of parameters
            cv_score = sample_loss(*next_sample)

            if cv_score > 0:
                iterations += 1

            # Update lists
            x_list.append(next_sample)
            y_list.append(cv_score)

            # Update xp and yp
            xp = np.array(x_list)
            yp = np.array(y_list)
        print("Optimized:")
        print(xp)
        print(yp)
        pair = xp, yp  # just a list of hyperparameter sets and their results
        return pair


setup_without_user_input()
training_time = 60 * 6
num_attempts = math.floor(training_time / Model.evolution_time)
param_bounds = np.array([[1, 1000], [1, 50], [0, 0.2], [-0.05, 0.05]])
training_result = Bayes.bayesian_optimisation(num_attempts, Bayes.run_parameter_set, param_bounds)
Writer.save_pickled_object(training_result, "train.txt")
