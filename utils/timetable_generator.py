import random

class TimetableGenerator:
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    SLOTS = ["S1", "S2", "S3", "S4", "S5"]

    def generate(self, courses, faculties, rooms):
        fac_map = {f['user_id']: f for f in faculties}
        course_list = []
        for c in courses:
            course_list.append({
                "course_id": c["course_id"],
                "course_name": c.get("course_name", ""),
                "eligible": c.get("eligible_faculty", []) or []
            })

        all_slots = [(d, s) for d in self.DAYS for s in self.SLOTS]
        random.shuffle(all_slots)

        timetable = []
        faculty_bookings = {}

        for course in course_list:
            elig = course["eligible"][:]
            if not elig:
                elig = [fid for fid, f in fac_map.items() if course["course_id"] in (f.get("courses") or [])]
            if not elig:
                elig = list(fac_map.keys())

            assigned = False
            attempts = 0
            while not assigned and attempts < 200:
                attempts += 1
                day, slot = random.choice(all_slots)
                fac_candidate = random.choice(elig)
                key = (fac_candidate, day, slot)
                if faculty_bookings.get(key):
                    continue
                room = random.choice(rooms)
                timetable.append({
                    "course_id": course["course_id"],
                    "course_name": course["course_name"],
                    "faculty_id": fac_candidate,
                    "faculty_name": fac_map.get(fac_candidate, {}).get("name", "TBD"),
                    "day": day,
                    "slot": slot,
                    "room": room
                })
                faculty_bookings[key] = True
                assigned = True

            if not assigned:
                timetable.append({
                    "course_id": course["course_id"],
                    "course_name": course["course_name"],
                    "faculty_id": None,
                    "faculty_name": "UNASSIGNED",
                    "day": "TBD",
                    "slot": "TBD",
                    "room": "TBD"
                })

        sort_order = {d: i for i, d in enumerate(self.DAYS)}
        timetable.sort(key=lambda x: (sort_order.get(x['day'], 999), x['slot']))
        return timetable
