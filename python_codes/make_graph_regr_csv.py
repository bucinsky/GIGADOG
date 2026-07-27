import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#                 C            D           E        F                  G             H              I            J              K
color_style = ["darkgrey","orange","olivedrab","palevioletred","mediumslateblue","goldenrod","mediumseagreen","salmon","cornflowerblue"]
bullets_style=["s","^","d","p","o","s","d","p","o"]

# read csv file
df = pd.read_csv("X_comparison_pds10_scores_sample.csv", sep=";")

# letters
df["letter"] = df["name"].str[0]
letters = ["C","D","E","F","G","H","I","J","K"]

# threshold
lim = -11

def make_scatter(fi, li, suffix):
    plt.figure(figsize=(5.5, 5.5))
    for i in reversed(range(fi, li)):
        L = letters[i]
        sub = df[df["letter"] == L]
        x = sub["DS"].values
        y = sub["avg_pds"].values
        
        # confusion matrix
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        
        for xs, ys in zip(x, y):

            # true positive
            if xs <= lim and ys <= lim:
                TP += 1
            # true negative
            elif xs > lim and ys > lim:
                TN += 1
            # false positive
            elif xs > lim and ys <= lim:
                FP += 1
            # false negative
            elif xs <= lim and ys > lim:
                FN += 1 

        # print results
        print(f"\n{L}")
        print(f"TP = {TP}")
        print(f"TN = {TN}")
        print(f"FP = {FP}")
        print(f"FN = {FN}")

        # recall and precision
        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0

        print(f"Precision =", round(precision,3))
        print(f"Recall    =", round(recall,3))
        
        #label2 = f"{L} ({len(x)})"
        label2 = f"{L} ({len(x):,})"
        plt.scatter(x, y, marker=bullets_style[i], color=color_style[i], s=4, label=label2)

    # axis limits
    x_min = -15
    x_max = -5
    y_min = -15
    y_max = -9.7

    # diagonal
    plt.plot([x_min, x_max], [x_min, x_max], 'k', linestyle='solid')
    plt.plot([x_min, x_max], [x_min-2, x_max-2], 'k', linestyle='dashed')
    plt.plot([x_min, x_max], [x_min+2, x_max+2], 'k', linestyle='dashed')

    # threshold lines
    plt.axvline(x=lim, linewidth=1.5, linestyle="dotted", color='black')
    plt.axhline(y=lim, linewidth=1.5, linestyle="dotted", color='black')

    # labels
    plt.gca().set(xlabel=r'$\mathrm{DS\ [kcal/mol]}$')
    plt.gca().set(ylabel=r'$\mathrm{PDS_{avg}\ [kcal/mol]}$')

    # axis control
    axes = plt.gca()
    axes.set_xlim([x_min, x_max])
    axes.set_ylim([y_min, y_max])

    # legend
    plt.legend(markerscale=3)

    # save
    png_name = f"plot_AK_united_{suffix}.png"
    eps_name = f"plot_AK_united_{suffix}.eps"

    plt.savefig(png_name, dpi=300)
    plt.savefig(eps_name, format='eps')
    plt.close()


# select which groups to plot
# uncomment only ONE option at a time

# C-F
#fi = 0
#li = 4
#make_scatter(fi, li, "C_to_F")

# G-K
fi = 4
li = 9
make_scatter(fi, li, "G_to_K")


