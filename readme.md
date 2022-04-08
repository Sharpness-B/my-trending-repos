## Dynamically display the activity of you repositories

```html
<img src="https://my-trending-repos.herokuapp.com/<github username>">
```

## Optional url parameters

Input a number of days to `timespanDays` to specify how old commits the illustration should include. The default value is 365.

Determine how many days the x-axis to group together by applying `setting` with one of the following `[day, week, month, year]`. The default value is month.


```html
<img src="https://my-trending-repos.herokuapp.com/sharpness-b?timespanDays=365&setting=month">
```

![example image](static/example.png?raw=true)

## Tech stack
 - Github api
 - Flask
 - Multiprocessing