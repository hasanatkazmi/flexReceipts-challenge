#!/usr/bin/env python

import json
import requests

base_url = 'http://localhost:3333/'


def create_metric(metric):
    return requests.post(base_url + 'create/' + metric)


def record_metric(metric, val):
    return requests.post(base_url + 'record/' + metric + '/' + str(val))


def get_summary(metric):
    return requests.get(base_url + 'statistics/' + metric)


def run_test():
    matric_name = 'first_matric'
    r = get_summary(matric_name)
    assert(r.status_code == 204)
    r = create_metric(matric_name)
    assert(r.status_code == 201)
    r = create_metric(matric_name)
    assert(r.status_code == 409)
    r = get_summary(matric_name)
    assert(r.status_code == 204)
    r = record_metric(matric_name, 5)
    assert(r.status_code == 204)
    r = record_metric(matric_name, 5)
    assert(r.status_code == 204)
    r = record_metric(matric_name, 1)
    assert(r.status_code == 204)
    r = record_metric(matric_name, 3)
    assert(r.status_code == 204)
    r = record_metric(matric_name, 1)
    assert(r.status_code == 204)
    r = record_metric(matric_name, -3)
    assert(r.status_code == 204)
    r = get_summary(matric_name)
    assert(r.status_code == 200)
    json = r.json()
    assert(json['max'] == 5)
    assert(json['min'] == -3)
    assert(json['median'] == 2)
    assert(json['mean'] == 2)

    matric_name = '2nd_matric'
    r = create_metric(matric_name)
    assert(r.status_code == 201)
    r = record_metric(matric_name, 1)
    r = get_summary(matric_name)
    assert(r.status_code == 200)
    json = r.json()
    assert(json['max'] == 1)
    assert(json['min'] == 1)
    assert(json['median'] == 1)
    assert(json['mean'] == 1)

if __name__ == '__main__':
    print "Restart the server before rerunning these tests because some status codes will be different on subsequent runs unless we restart the server"
    run_test()
    print "Tests ran successfully"
