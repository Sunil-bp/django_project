import datetime
print(datetime.datetime.now())


yesterday = datetime.date.today()
t = datetime.time(hour=23, minute=30)
d3 = datetime.datetime.combine(yesterday, t)
print(d3)

ow = datetime.datetime.now(datetime.timezone.utc)
print(ow)
# datetime.datetime(2020, 2, 19, 12, 17, 2, tzinfo=<UTC>)
# >>>