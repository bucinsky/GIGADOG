# import modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#                 C            D           E        F                  G             H              I            J              K
color_style = ["darkgrey","orange","olivedrab","palevioletred","mediumslateblue","goldenrod","mediumseagreen","salmon","cornflowerblue"]

# read csv file
df = pd.read_csv("X_comparison_pds10_scores_sample.csv", sep=";")

# letters
df["letter"] = df["name"].str[0]
letters = ["C","D","E","F","G","H","I","J","K"]

# bins
bin_default = np.arange(-15, -5, 1)


def make_histogram(fi, li, suffix):
    plt.figure(figsize=(5.5, 5.5))

    xs = []
    label2 = []
    color2 = []

    for i in range(fi, li):
        L = letters[i]

        sub = df[df["letter"] == L]
        y = sub["DS"].values

        xs.append(y)
        label2.append(f"{L} ({len(y):,})")
        color2.append(color_style[i])

    plt.hist(xs, bins=bin_default, color=color2, label=label2, histtype='bar', log=True, rwidth=0.7)
    plt.xticks(np.arange(-15, -4, 1))
    plt.xlim(-15, -5)
    
    plt.ylim(0.5, 1e4)
    
    plt.gca().set(xlabel=r'$\mathrm{DS\ [kcal/mol]}$')
    plt.legend()

    plt.savefig(f"histogram_AK_united_{suffix}_DS_all.png", dpi=300)
    plt.savefig(f"histogram_AK_united_{suffix}_DS_all.eps", format='eps')
    plt.close()


# select the range of letters to plot.
# uncomment only ONE section below

# C–F
#fi = 0
#li = 4
#make_histogram(fi, li, "C_to_F")

# G–K
fi = 4
li = 9
make_histogram(fi, li, "G_to_K")


