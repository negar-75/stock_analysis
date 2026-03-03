logs = [
    ("payment", "FAIL"),
    ("auth", "SUCCESS"),
    ("payment", "FAIL"),
    ("auth", "FAIL"),
    ("payment", "SUCCESS"),
    ("auth", "FAIL"),
]

output = {i[0]: {"FAIL": 0, "SUCCESS": 0} for i in logs}
for log in logs:
    key = log[0]
    if key in output.keys():
        output[key][log[1]] += 1


# {
#     "payment": {"failure": 0 ,"success":6}
#     "auth": {"failure": 0 ,"success":6}
# }

print(output)
