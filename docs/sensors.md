# Sensors
Depending on the type you defined, you will get several sensors.

## Basket
The sensor `jumbo_basket` indicates how many items you still have within your basket. Within the more dialog window you will also see the outstanding costs that you have.

#### Attributes
| Name | Example | Description |
|------|---------|-------------|
| currency | EUR | Currency being used |
| amount | 5.00 | Current price |
| format | EUR 5.00 | Full price format |

## Live
The sensor `jumbo_live` indicates the live arrival date of your next upcoming delivery. Most of the time, this sensor will be in an `Unknown` state as it will only contain a time when Jumbo shared the arrival time. However, as soon as the time is known, the state will change to the actual live time.

#### Attributes
| Name | Example | Description |
|------|---------|-------------|
| eta_start | 11:00 | Start time of the delivery window. More precise then the actual time slot |
| eta_end | 12:00 | End time of the delivery window. More precise then the actual time slot |

## Deliveries
The sensor `jumbo_delivery` indicates the state of your next upcoming delivery. See [States](states.md) for potential states.
Within the attributes (more info dialog), you can also see any future deliveries.

#### Attributes
The attributes contains a `deliveries` array, which shows all your open deliveries. Below is a description of an entire delivery object.

| Name | Example | Description |
|------|---------|-------------|
| id | 2069233530 | ID of the order |
| status | open | Status of the order. See [States](states.md) |
| time | 10:00 - 13:00 | Delivery window |
| date | 2021-03-29 | Date of the delivery |
| start_time | 10:00 | Start time of the delivery window |
| end_time | 13:00 | End time of the delivery window |
| cut_off_date | 2021-03-27T12:00:00 | The date when your order closes and you no longer can alter / cancel it |
| eta_start | 11:00 | Once your order is on it's way, this is the start time of the delivery window. Potentially use the `sensor.jumbo_live` in such case. |
| eta_end | 12:00 | Once your order is on it's way, this is the end time of the delivery window. Potentially use the `sensor.jumbo_live` in such case. |
| eta_live | 11:19 | Once your order is on it's way, this is the live time of the delivery window. Potentially use the `sensor.jumbo_live` in such case. |
| price.currency | EUR | Currency being used |
| price.amount | 5.00 | Current price |
| price.format | EUR 5.00 | Full price format |

## Delivery time slots
The sensor `jumbo_delivery_time_slots` indicates the next available delivery time slot. Within the attributes (more info dialog), you can also see any future delivery time slots.

#### Attributes
The attributes contains a `time_slots` array, which shows all available time slots. Below is a description of an entire time slot object.

| Name | Example | Description |
|------|---------|-------------|
| type | homedelivery | Type of the time slot |
| start_date_time | 2021-03-30T18:00:00 | Start date of the time slot |
| end_date_time | 2021-03-30T21:00:00 | End date of the time slot |
| available | true | Indicates if the time slot is available |
| price.currency | EUR | Currency being used |
| price.amount | 5.00 | Current price |
| price.format | EUR 5.00 | Full price format |

## Pick ups
The sensor `jumbo_pick_up` indicates the state of your next upcoming pick up. See [States](states.md) for potential states.
Within the attributes (more info dialog), you can also see any future pick ups.

#### Attributes
The attributes contains a `pick_ups` array, which shows all your open pick ups. Below is a description of an entire pick up object.

| Name | Example | Description |
|------|---------|-------------|
| id | 2069233530 | ID of the order |
| status | open | Status of the order. See [States](states.md) |
| time | 10:00 - 13:00 | Pick up window |
| date | 2021-03-29 | Date of the pick up |
| start_time | 10:00 | Start time of the pick up window |
| end_time | 13:00 | End time of the pick up window |
| cut_off_date | 2021-03-27T12:00:00 | The date when your order closes and you no longer can alter / cancel it |
| price.currency | EUR | Currency being used |
| price.amount | 5.00 | Current price |
| price.format | EUR 5.00 | Full price format |

## Pick up time slots
The sensor `jumbo_pick_up_time_slots` indicates the next available pick up time slot. Within the attributes (more info dialog), you can also see any future pick up time slots.

#### Attributes
The attributes contains a `time_slots` array, which shows all available time slots. Below is a description of an entire time slot object.

| Name | Example | Description |
|------|---------|-------------|
| type | homedelivery | Type of the time slot |
| start_date_time | 2021-03-30T18:00:00 | Start date of the time slot |
| end_date_time | 2021-03-30T21:00:00 | End date of the time slot |
| available | true | Indicates if the time slot is available |
| price.currency | EUR | Currency being used |
| price.amount | 5.00 | Current price |
| price.format | EUR 5.00 | Full price format |