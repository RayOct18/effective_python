from datetime import datetime, timedelta


class Bucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0
    
    def __repr__(self):
        return f'Bucket(quota={self.quota})'

def fill(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount

def deduct(bucket, amount):
    now = datetime.now()
    if (now - bucket.reset_time) > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


class NewBucket:
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0
    
    def __repr__(self):
        return (f'NewBuck(max_quota={self.max_quota}, '
                f'quota_consumed={self.quota_consumed})')
    
    @property
    def quota(self):
        return self.max_quota-self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


if __name__ == '__main__':
    bucket = Bucket(60)
    fill(bucket, 100)
    print(bucket)
    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
    print(bucket)
    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
    print(bucket)

    bucket = NewBucket(60)
    fill(bucket, 100)
    print(bucket)
    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
    print(bucket)
    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
    print(bucket)
