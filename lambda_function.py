import gspread
import json


def post(event, sheet):
    eventbody = json.loads(event["body"])
    params = {"valueInputOption": "USER_ENTERED"}
    sheetrange = "Sheet1!A:A"
    body = {
        "majorDimension": "ROWS",
        "values": [[eventbody["userName"], eventbody["userTime"]]]
    }
    sheet.values_append(sheetrange, params, body)
    return {
        "statusCode": 201,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps("success")
    }


def get(wsheet):
    names = wsheet.col_values(3)
    times = wsheet.col_values(4)

    def chefjson(data1, data2):
        return {"userName": data1, "userTime": data2}

    ls_data = []
    i = 0
    for x in names:
        ls_data.append(chefjson(x, times[i]))
        i += 1
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(ls_data)
    }


def lambda_handler(event, context):
    gc = gspread.service_account(filename='creds.json')
    sheetobj = gc.open('Database')
    wsheet = sheetobj.sheet1
    if event["httpMethod"] == "POST":
        return post(event, sheetobj)
    elif event["httpMethod"] == "GET":
        return get(wsheet)
    else:
        return {
            "statusCode": 405,
            "body": json.dumps("Method not allowed")
        }
