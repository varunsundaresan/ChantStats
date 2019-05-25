import palettable
from .unit import UnitType

## The following are based on the "Categorical color scale generator (HCL)" (http://bl.ocks.org/nitaku/8566245)
# color_palette = ["#ed5e93", "#e76b4f", "#ba881d", "#779d2c", "#00a76a", "#00aab3", "#00a3ec", "#4191f9", "#bf73d5"]
# color_palette = ["#ff7aad", "#ff8668", "#d8a23a", "#92b847", "#00c384", "#00c6cf", "#00bfff", "#66abff", "#dc8df2"]
# color_palette = ["#ef8ead", "#ec957e", "#cda563", "#9db46b", "#61bc91", "#00bec3", "#28b8e9", "#89abf2", "#cd99da"]

## Tableau-based color palette
tableau_medium_10 = palettable.tableau.TableauMedium_10.hex_colors
tableau_medium_10_8 = [
    "#729ECE",
    #'#FF9E4A',
    "#67BF5C",
    "#ED665D",
    "#AD8BC9",
    "#A8786E",
    "#ED97CA",
    "#A2A2A2",
    #'#CDCC5D',
    "#6DCCDA",
]

## Matplotlib Viridis
# viridis_15 = palettable.matplotlib.Viridis_15.hex_colors
viridis_15_8 = [
    #'#440154',
    #'#481B6D',
    #'#46327E',
    "#3F4889",
    "#365C8D",
    "#2E6E8E",
    "#277F8E",
    "#21918C",
    "#1FA187",
    "#2DB27D",
    "#4AC16D",
    #'#70CF57',
    #'#A0DA39',
    #'#D0E11C',
    #'#FDE725'
]
viridis_15_12 = [
    #'#440154',
    #'#481B6D',
    "#46327E",
    "#3F4889",
    "#365C8D",
    "#2E6E8E",
    "#277F8E",
    "#21918C",
    "#1FA187",
    "#2DB27D",
    "#4AC16D",
    "#70CF57",
    "#A0DA39",
    "#D0E11C",
    #'#FDE725'
]

viridis_12 = palettable.matplotlib.Viridis_12.hex_colors
viridis_12_8 = [
    #'#440154',
    #'#482173',
    "#433E85",
    "#38598C",
    "#2D708E",
    "#25858E",
    "#1E9B8A",
    "#2AB07F",
    "#50C46A",
    "#86D549",
    #'#C2DF23',
    #'#FDE725'
]

## Matplotlib Plasma
plasma_15 = palettable.matplotlib.Plasma_15.hex_colors
plasma_15_8 = [
    #'#0D0887',
    #'#350498',
    #'#5302A3',
    #'#7100A8',
    "#8B0AA5",
    "#A31E9A",
    "#B83289",
    "#CC4778",
    "#DB5C68",
    "#E97158",
    "#F48849",
    "#FBA139",
    #'#FEBD2A',
    #'#FADA24',
    #'#F0F921'
]

plasma_12 = palettable.matplotlib.Plasma_12.hex_colors
plasma_12_8 = [
    #'#0D0887',
    #'#3E049C',
    # "#6300A7",
    "#8707A6",
    "#A62098",
    "#C03A83",
    "#D5546E",
    "#E76F5A",
    "#F58C46",
    "#FDAE32",
    "#FCD225",
    #'#F0F921'
]

# inferno_12_8 = [
#     #'#000004',
#     #'#140B34',
#     "#390963",
#     "#61136E",
#     "#85216B",
#     "#A92E5E",
#     "#CB4149",
#     "#E65D2F",
#     "#F78212",
#     "#FCAE12",
#     #'#F5DB4C',
#     #'#FCFFA4'
# ]


def get_color_palette_for_unit(unit):
    unit = UnitType(unit)
    if unit.value == "pcs":
        # # return palettable.cartocolors.qualitative.Vivid_8.hex_colors
        # return palettable.cartocolors.qualitative.Vivid_9.hex_colors
        # return plasma_12_8
        return tableau_medium_10_8
    elif unit.value == "mode_degrees":
        # # return palettable.cartocolors.qualitative.Pastel_10.hex_colors
        # return palettable.colorbrewer.qualitative.Set3_12.hex_colors
        # # return palettable.matplotlib.Viridis_12.hex_colors
        # # return palettable.tableau.PurpleGray_12.hex_colors
        # # return sns.color_palette("muted", 12).as_hex()  # WARNING: this contains only 10 distinct colors!!!
        return viridis_15_12
    else:
        raise ValueError(f"Unexpected value: {unit.value}")
