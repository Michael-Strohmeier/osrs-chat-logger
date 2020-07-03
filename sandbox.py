import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv("15937240589150908.csv")
    df.drop_duplicates(["time", "name"], keep='last')

    print(df)
