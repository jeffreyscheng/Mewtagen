from dialgarithm.evolve import *
import math
import numpy as np
import sklearn.gaussian_process as gp
from scipy.stats import norm
from scipy.optimize import minimize


class Bayes:
    time_per_battle = 20 / 1000  # from EC2 instance and personal laptop
    target_time = 5 * 60

    @staticmethod
    def run_parameter_set(population_size, matches, starting_mutation_rate, mutation_delta):
        population_size = math.floor(population_size)
        matches = math.floor(matches)
        time_for_final_evaluation = Bayes.time_per_battle * population_size * max(25.0, 2 * matches)
        time_for_evolution = Bayes.target_time - time_for_final_evaluation
        if time_for_evolution <= 0 or population_size <= 0 or matches <= 0 or starting_mutation_rate <= 0:
            print("not enough time!")
            print(time_for_final_evaluation)
            return 0
        else:
            time_per_generation = population_size * matches * Bayes.time_per_battle
            num_generations = math.floor(time_for_evolution / time_per_generation)
            print(num_generations)

            # TODO: DO THING SOMETHING FUNCTION
            def something(a, b, c, d, e):
                pass

            attempts = sorted([something() for _ in range(0, 5)])
            return attempts[2]

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
            expected_improvement[sigma == 0.0] == 0.0

        return -1 * expected_improvement

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
        best_x = None
        best_acquisition_value = 1
        n_params = bounds.shape[0]

        for starting_point in np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_restarts, n_params)):

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

        x_list = []
        y_list = []

        n_params = bounds.shape[0]

        if x0 is None:
            for params in np.random.uniform(bounds[:, 0], bounds[:, 1], (n_pre_samples, bounds.shape[0])):
                x_list.append(params)
                y_list.append(sample_loss(params))
        else:
            for params in x0:
                x_list.append(params)
                y_list.append(sample_loss(params))

        xp = np.array(x_list)
        yp = np.array(y_list)

        # Create the GP
        if gp_params is not None:
            model = gp.GaussianProcessRegressor(**gp_params)
        else:
            kernel = gp.kernels.Matern()
            model = gp.GaussianProcessRegressor(kernel=kernel,
                                                alpha=alpha,
                                                n_restarts_optimizer=10,
                                                normalize_y=True)

        for n in range(n_iters):

            model.fit(xp, yp)

            # Sample next hyperparameter
            if random_search:
                x_random = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(random_search, n_params))
                ei = -1 * expected_improvement(x_random, model, yp, greater_is_better=True, n_params=n_params)
                next_sample = x_random[np.argmax(ei), :]
            else:
                next_sample = sample_next_hyperparameter(expected_improvement, model, yp, greater_is_better=True,
                                                         bounds=bounds, n_restarts=100)

            # Duplicates will break the GP. In case of a duplicate, we will randomly sample a next query point.
            if np.any(np.abs(next_sample - xp) <= epsilon):
                next_sample = np.random.uniform(bounds[:, 0], bounds[:, 1], bounds.shape[0])

            # Sample loss for new set of parameters
            cv_score = sample_loss(next_sample)

            # Update lists
            x_list.append(next_sample)
            y_list.append(cv_score)

            # Update xp and yp
            xp = np.array(x_list)
            yp = np.array(y_list)

        return xp, yp

target_time = 10 * 60 # change to 20-24 hours
time_per_attempt = 5 * 60
num_attempts = target_time / time_per_attempt
# Bayes.bayesian_optimisation(num_attempts, Bayes.run_parameter_set, TODO: bounds)