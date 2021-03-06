from typing import Dict, Tuple
import pandas as pd
import seaborn as sns
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt


def generate_account_visualization(
    account: Dict[str, Tuple[str, int]],
    dest_folder="images",
    num_cols=16,
    title=None,
    **sns_kwargs,
):
    rows = []
    step = min([size for _, size in account.values()])
    for field, (data_type, size) in account.items():
        for _ in range(0, size, step):
            rows.append([f"{field}: {data_type}"])
    df = pd.DataFrame(rows, columns=["field"])
    labels = list(reversed(df["field"].unique().tolist()))
    field_to_idx = dict([(c, i) for i, c in enumerate(labels)])
    df["row"] = (df.index // int(num_cols)) * num_cols * step
    df["col"] = ((df.index % num_cols) + 1) * step
    vis_df = df.set_index("row").pivot(columns="col").field.replace(field_to_idx)
    diff = vis_df.diff()
    vis_df = vis_df[
        (diff.abs().sum(axis=1) != 0) | ((diff == diff).sum(axis=1) != vis_df.shape[1])
    ]
    plt.rcParams.update({"font.size": 18, "font.family": "Futura", "axes.labelpad": 15})
    size = 1
    cbar_size = 0.5
    nrows, ncols = vis_df.shape
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(ncols * size + cbar_size, nrows * size),
        gridspec_kw={"width_ratios": [ncols * size, cbar_size]},
    )
    ax = axes[0]
    sns.heatmap(
        vis_df.replace(field_to_idx),
        annot=None,
        fmt="",
        ax=ax,
        linewidths=0.5,
        cbar_ax=axes[1],
        cmap=sns.color_palette(n_colors=len(account)),
        **sns_kwargs,
    )
    cbar = ax.collections[0].colorbar
    r = cbar.vmax - cbar.vmin
    title_font_size = 3 * num_cols
    label_font_size = 2 * num_cols
    major_ax_font_size = num_cols
    minor_ax_font_size = int(0.7 * num_cols)
    labelpad = num_cols
    start = 1 / (2 * len(account))
    end = 1 - start
    cbar.set_ticks([(r * i) + cbar.vmin for i in np.linspace(start, end, len(labels))])
    cbar.set_ticklabels(labels)
    cbar.ax.set_title("Field", pad=15)
    cbar.ax.tick_params(axis="both", which="major", labelsize=major_ax_font_size)
    cbar.ax.tick_params(axis="both", which="minor", labelsize=minor_ax_font_size)
    ax.set_xticks(np.arange(vis_df.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(vis_df.shape[0]) + 0.5, minor=False)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.set_xticklabels([f"+{x}" for x in vis_df.columns.tolist()], minor=False)
    yticklabels = []
    for curr, prev in zip(vis_df.index[1:], vis_df.index):
        if curr - prev != step * num_cols:
            yticklabels.append(f"{prev} - {curr}")
        else:
            yticklabels.append(f"{prev}")
    yticklabels.append(str(vis_df.index[-1]))
    ax.set_yticklabels(yticklabels, minor=False)
    ax.tick_params(axis="y", labelrotation=0)
    ax.set_xlabel(None)
    ax.set_ylabel(
        "Buffer Index",
        size=label_font_size,
        labelpad=labelpad,
        weight="semibold",
        family="Futura",
    )
    ax.tick_params(axis="both", which="major", labelsize=major_ax_font_size)
    ax.tick_params(axis="both", which="minor", labelsize=minor_ax_font_size)
    plt.tight_layout()
    nrows = vis_df.shape[0]
    plt.subplots_adjust(top=1 - (1.5 / nrows))
    if title:
        ax.set_title(title, fontsize=title_font_size, pad=20)
        plt.savefig(dest_folder + "/" + title.lower().replace(" ", "_") + ".png")
    else:
        plt.show()


if __name__ == "__main__":
    token_account = OrderedDict(
        mint=("Pubkey", 32),
        owner=("Pubkey", 32),
        amount=("u64", 8),
        delegate=("COption<Pubkey>", 36),
        state=("AccountState", 1),
        is_native=("COption<u64>", 12),
        delegated_amount=("u64", 8),
        close_authority=("COption<Pubkey>", 36),
    )
    mint = OrderedDict(
        mint_authority=("Pubkey", 32),
        supply=("u64", 8),
        decimals=("u8", 1),
        is_initialized=("bool", 1),
        freeze_authority=("COption<Pubkey>", 36),
    )
    generate_account_visualization(token_account, title="Token Account Layout")
    generate_account_visualization(mint, title="Mint Layout")

    token_metadata = OrderedDict(
        key=("Key", 1),
        update_authority=("Pubkey", 32),
        mint=("Pubkey", 32),
        name_size=("usize", 4),
        name=("String", 32),
        symbol_size=("usize", 4),
        symbol=("String", 10),
        uri_size=("usize", 4),
        uri=("String", 200),
        seller_fee_basis_points=("u16", 2),
        creators_flag=("bool", 1),
        creators_size=("usize", 4),
        creator0_pubkey=("Pubkey", 32),
        creator0_verified=("bool", 1),
        creator0_share=("u8", 1),
        creator1_pubkey=("Pubkey", 32),
        creator1_verified=("bool", 1),
        creator1_share=("u8", 1),
        creator2_pubkey=("Pubkey", 32),
        creator2_verified=("bool", 1),
        creator2_share=("u8", 1),
        creator3_pubkey=("Pubkey", 32),
        creator3_verified=("bool", 1),
        creator3_share=("u8", 1),
        creator4_pubkey=("Pubkey", 32),
        creator4_verified=("bool", 1),
        creator4_share=("u8", 1),
        primary_sale_happened=("bool", 1),
        is_mutable=("bool", 1),
        edition_nonce=("Option<u8>", 5),
        padding=("bytes", 176),
    )
    generate_account_visualization(token_metadata, title="Token Metadata Layout")
