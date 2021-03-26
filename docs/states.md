## States
Here is the list through which states a delivery / pick up goes:

| State | Description | When |
|-------|-------------|------|
| open  | You can still change your order | As soon as you open up an order |
| processing | You cannot change your order, but it's not ready yet for delivery / pick up | As soon as the cut off date has been reached |
| ready_to_deliver | Jumbo is about to deliver your order. | As soon as the time slot time is reached |
| ready_to_pick_up | You can almost pick up your order. | As soon as the time slot time is reached. Note: UNTESTED |
| picked_up | The order is closed | As soon as you picked up the order or when the order was delivered |
| cancelled | The order is cancelled | As soon as you cancelled the order |