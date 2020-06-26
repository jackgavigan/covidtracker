

def region_data(new_cases, populations):
    history_days = 45
    weekly_cases = new_cases.rolling(date=7).sum()

    cases = {}
    for gss_code in weekly_cases["gss_code"].values:
        this_week = int(weekly_cases.sel(gss_code=gss_code).values[-1])
        history = new_cases[:, -history_days:].sel(gss_code=gss_code).values
        cases[gss_code] = {
            "prevalence": (this_week / populations[gss_code]),
            "cases": this_week,
            "history": list(map(int, history)),
        }
    return cases


def map_data(
    eng_data, wales_data, scot_data, populations, scot_populations, provisional_days
):
    scot_data = scot_data.drop_sel(gss_code="S92000003")
    eng_new_cases = (
        eng_data["cases"].ffill("date").fillna(0)[:, :-provisional_days].diff("date")
    )
    wales_new_cases = (
        wales_data["cases"].ffill("date").fillna(0)[:, :-provisional_days].diff("date")
    )
    scot_new_cases = scot_data["corrected_cases"].ffill("date").fillna(0).diff("date")

    cases_england = region_data(eng_new_cases, populations)
    cases_wales = region_data(wales_new_cases, populations)
    cases_scotland = region_data(scot_new_cases, scot_populations)
    return {"england": cases_england, "scotland": cases_scotland, "wales": cases_wales}
