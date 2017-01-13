flexReciepts challenge
===============
**Requirements:**
Python 2.7

**To Run:**
```
>>python flexReciepts.py
```

It will print instructions for tearing down the server.

To run automated test:
```
>>python flexReciepts-test.py
```
It will test few scenarios and test if outcome is correct and expected.

**API**: 


|                  |                        | 
 ----------------- | ---------------------------- | 
| Endpoint | `/create/<metric>`            |
| Description          | `Creates the metric`            |
| Method           | `POST`            |
| Body           | `None`            |
| Status code: 201           | `Metric created` |
| Status code: 400           | `Unexpected or unspecified URI` |
| Status code: 409           | `Metric already created` |

|                  |                        | 
 ----------------- | ---------------------------- | 
| Endpoint | `/record/<metric>/<value>`            |
| Description          | `Post value to the metric`            |
| Method           | `POST`            |
| Body           | `None`            |
| Status code: 204           | `Value saved for metric` |
| Status code: 400           | `Unexpected or unspecified URI or metric not registered` |


|                  |                        | 
 ----------------- | ---------------------------- | 
| Endpoint 		| `/statistics/<metric>`            |
| Description          | `Get statistics of the metric`            |
| Method           | `GET`            |
| Body           | `JSON (format mentioned below) or None if summary can not be produced`  |
| Status code: 204           | `Metric not registered or there are no values to generate statistics for the given metric` |
| Status code: 200           | `Success. Summary is in the body` |


**JSON format for summary:**

    {
	    "max": numeric - maximum value for the given metric , 
	    "mean": double - average value of all values for given metric, 
	    "median": double - median value of all values for given metric, 
	    "min": numeric - maximum value for the given metric
    }