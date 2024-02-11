import time


def now():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def dataframe_to_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)
