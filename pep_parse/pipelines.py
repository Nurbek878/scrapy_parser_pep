import csv
from datetime import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


class PepParsePipeline:

    def open_spider(self, spider):
        self.status = {}

    def process_item(self, item, spider):
        status_pep = item['status']
        if status_pep in self.status:
            self.status[status_pep] += 1
        else:
            self.status[status_pep] = 1
        return item

    def close_spider(self, spider):
        results = BASE_DIR / 'results'
        results.mkdir(exist_ok=True)
        time = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = results / f'status_summary_{time}.csv'
        with open(filename, mode='w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Статус', 'Количество'])
            writer.writerows(self.status.items())
            total = sum(self.status.values())
            writer.writerow(['Total', total])
