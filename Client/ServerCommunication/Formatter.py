

def format_message(data_type, data):
    data = ", ".join(str(d) for d in data)

    result = f"{data_type}; {data}"

    return result



def decode(input):
    data_type, data = input.split(";")

    input = data_type.strip()
    data = [item.strip() for item in data.split(",")]

    return data_type, data
