from utils.ExtractCardContent import extractCardContent
from utils.ThousandConversion import thousandsConversion

def cardFormatting(visual):

    cardContent = visual["VisualData"]["data"]

    formattedData = extractCardContent(cardContent)

    cardData = {
        "Title": "",
        "Content": "",
        "DyamicValue": "",
        "DynamicVariance": "",
        "ContentColor": "",
        "DynamicTitle": "",
    }

    cardData["Title"] =  visual["Title"]
    cardData["Content"] = formattedData[1]

    # if (
    #     visual["Title"].lower() == "open pipeline"
    #     or visual["Title"].lower() == "avg. deal size"
    # ):
        
    #     cardContent["Content"] = thousandsConversion(formattedData[1], "$")
    # else:
    #     cardData["Content"] = formattedData[1]
    # print(cardData,"dbfdfb")

    return cardData

