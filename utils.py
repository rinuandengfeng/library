# 分割座位号
def seatid_to_json(raw_seat_id, raw_seat_num):
    seat_dict ={}
    for i in range(0,len(raw_seat_id)):
        seat_id = raw_seat_id[i].split("_")[1]
        seat_dict[seat_id] = raw_seat_num[i]
    return seat_dict