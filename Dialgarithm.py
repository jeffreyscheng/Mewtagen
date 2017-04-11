class Dialgarithm:
    gen = None
    format = None
    dex = None
    moveset_dict = None # -> usage statistics
    metagame = None
    recommendations = None

    @staticmethod
    def set_meta(gen, meta_format):
        Dialgarithm.gen = gen
        Dialgarithm.format = meta_format

