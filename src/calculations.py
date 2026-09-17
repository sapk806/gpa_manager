import pandas as pd
import numpy as np

class Calculator():
    def course_grade(self, df: pd.DataFrame):
        overall_grade = 0
        overall_weight = 0
        for category in set(df["category"]):
            num = (df.loc[df["category"] == category]["earned_points"].sum())
            den = (df.loc[df["category"] == category]["max_points"].sum())
            category_grade = num / den * df.loc[df["category"] == category]["weight"].iloc[0]*100
            overall_grade += category_grade
            overall_weight += df.loc[df["category"] == category]["weight"]
        return (overall_grade / overall_weight).iloc[0]
    def overall_gpa(self, gpas: list):
        overall = 0
        credits = 0
        for gpa in gpas:
            if gpa[0] == 'A':
                overall += (4.0 * gpa[1])
            elif gpa[0] == 'B':
                overall += (3.0 * gpa[1])
            elif gpa[0] == 'C':
                overall += (2.0 * gpa[1])
            elif gpa[0] == 'D':
                overall += (1.0 * gpa[1])
            credits += gpa[1]
        return overall/credits