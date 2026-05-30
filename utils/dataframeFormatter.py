import pandas


def renameColumn(dataFrame: pandas.DataFrame, columnsToRename: list[str], renameValue: str):
    try:
        nbrChange = 0
        errorMessage = ""
        for elem in columnsToRename:
            if elem in dataFrame:
                if nbrChange == 1:
                    errorMessage = "multiple column with same name meaning " + renameValue
                    return dataFrame, errorMessage + "\n"
                dataFrame = dataFrame.rename(columns={elem: renameValue})
                nbrChange += 1
    except Exception as ex:
        return dataFrame, str(ex)

    return dataFrame, errorMessage


def formatDataFrame(
    dataFrame: pandas.DataFrame,
    columnsToRename: list[str],
):
    errorMessage = ""

    for column in columnsToRename:
        errorMessageFunction = ""
        possibleName = listNamingConventionFromSnakeCase(column)
        dataFrame, errorMessageFunction = renameColumn(dataFrame, possibleName, column)
        errorMessage += errorMessageFunction

    return dataFrame, errorMessage


def listNamingConventionFromSnakeCase(snakeCaseVar: str) -> list[str]:
    splitName: list[str] = snakeCaseVar.split("_")
    variationList: list[str] = []

    variationList.append(snakeCaseVar)

    screaminSnake = "_".join([word.upper() for word in splitName])
    variationList.append(screaminSnake)

    camel = splitName[0] + "".join([word.capitalize() for word in splitName[1:]])
    variationList.append(camel)

    pascal = "".join([word.capitalize() for word in splitName])
    variationList.append(pascal)

    kebab = "-".join(splitName)
    variationList.append(kebab)

    train = "-".join([word.capitalize() for word in splitName])
    variationList.append(train)

    upperCase = "".join([word.upper() for word in splitName])
    variationList.append(upperCase)

    lowerCase = "".join([word.lower() for word in splitName])
    variationList.append(lowerCase)

    dot = ".".join(splitName)
    variationList.append(dot)

    spaced = " ".join(splitName)
    variationList.append(spaced)

    title = " ".join([word.title() for word in splitName])
    variationList.append(title)

    variationList = list(dict.fromkeys(variationList))

    return variationList
