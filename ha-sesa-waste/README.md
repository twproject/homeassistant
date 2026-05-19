# SESA Waste Collection for Home Assistant

Custom integration for reading the waste collection calendar from `app.sesaeste.it`.

## Installation

Copy:

```text
custom_components/sesa_waste
```

to:

```text
/config/custom_components/sesa_waste
```

Restart Home Assistant, then add the integration from:

```text
Settings > Devices & services > Add integration > SESA Waste Collection
```

## Entities

The integration creates:

- `sensor.sesa_next_waste`
- `sensor.sesa_tomorrow_waste`
- `calendar.sesa_waste_calendar`

The calendar contains one all-day event for each collection day.

## Notes

This integration uses the same HTTP endpoints used by the public SESA web app. It does not perform vulnerability scanning or intrusive testing.
