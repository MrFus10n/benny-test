import datetime
import re
import spacy
import typing as t

from spacy.cli.download import download as spacy_download


class Parser:
    contributions_keywords = {'contribution', 'amount', 'percentage', 'deduction', 'compensation', '%', '$'}
    periods_keywords = {'commence', 'start', 'begin', 'end', 'terminate', 'period', 'date', 'day', 'year', 'month'}
    periods_label = 'DATE'

    def __init__(self):
        model_name = 'en_core_web_sm'
        try:
            self.nlp = spacy.load(model_name)
        except OSError:
            spacy_download(model_name)
            self.nlp = spacy.load(model_name)

    @staticmethod
    def calculate_dates_distance(date_since: datetime.date, date_till: datetime.date) -> int:
        delta = date_till - date_since
        return min(abs(delta.days), 366 - abs(delta.days))

    def extract_amounts(self, text: str) -> t.Tuple[str, str]:
        # Remove special chars
        chars_to_remove = ',()'
        trans = str.maketrans('', '', chars_to_remove)
        text = text.translate(trans)

        # Find all the % and $ values in paragraph
        amounts = [
            word
            for word in text.split(' ')
            if word[0] == '$' or word[-1] == '%'
        ]
        percents = sorted([float(w[:-1]) for w in amounts if w[-1] == '%'])
        moneys = sorted([float(w[1:]) for w in amounts if w[0] == '$'])

        # Get min and max % and $ values
        min_amounts = [
            f'{percents[-2]}%' if len(percents) == 2 else None,
            f'${moneys[-2]}' if len(moneys) == 2 else None,
        ]
        max_amounts = [
            f'{percents[-1]}%' if percents else None,
            f'${moneys[-1]}' if moneys else None,
        ]

        # Format the output strings
        amount_min = ' or '.join([a for a in min_amounts if a])
        amount_max = ' or '.join([a for a in max_amounts if a])

        return amount_min, amount_max


    def extract_periods(self, text: str) -> t.List[t.List[datetime.date]]:
        """ Returns an array of [period_start, period_end] dates extracted from the text """
        month_pattern = (
            r'(?:January|February|March|April|May|June|Jun|July|Jul|August|September|October|November|December)'
        )
        day_pattern = r'\s\d{1,2}'
        not_year_pattern = r'(?!\s*\d{4})'

        # Find all dates that consist of month and day and not year
        pattern = r'\b' + month_pattern + day_pattern + not_year_pattern + r'\b'
        matches = re.findall(pattern, text)

        # No periods found
        if not matches:
            return []

        # Parse dates at leap year to have all the days available
        dates = [
            datetime.datetime.strptime(f'{d} 2004', '%B %d %Y')
            for d in matches
        ]

        # One period mentioned
        if len(dates) == 1:
            return [[dates[0], dates[0] - datetime.timedelta(days=1)]]

        # First mentioned date is for sure start (due to the language logic)
        start_date = dates[0]

        # All the rest of wording does not matter. Sort all unique dates starting with the first mentioned
        dates = list(set(dates))
        dates.sort()
        idx = dates.index(start_date)
        dates = dates[idx:] + dates[:idx] + [start_date]

        periods = []
        i = 0
        while i < len(dates)-1:
            period_start = dates[i]
            period_end = dates[i+1]  # Potential period end. Might be a start of the next one

            # The date after the period_end
            if i+2 < len(dates):
                next_date = dates[i+2]
            else:
                next_date = start_date

            days_till_next_date = self.calculate_dates_distance(period_end, next_date)

            # The next_date is the start of the next period, meaning period_end is correct
            if days_till_next_date == 1:
                periods.append([period_start, period_end])
                i += 2  # Start of the next period is next_date

            # period_end is really a start of the next period
            else:
                periods.append([period_start, period_end - datetime.timedelta(days=1)])
                i += 1  # Start of the next period is period_end

        return periods

    def find_contributions_paragraph(self,  paragraphs: t.Sequence[str]):
        """ Returns the content of the contributions paragraph """
        return self.find_paragraph(paragraphs, self.contributions_keywords)

    def find_paragraph(
        self,
        paragraphs,  # type: t.Sequence[str]
        keywords,  # type: t.Set[str]
        label=None  # type: str
    ) -> str:
        """ Returns the content of the paragraph with highest mentioning of keywords """
        ranks = []
        for paragraph in paragraphs:
            rank = 0
            paragraph = paragraph.lower()

            # Count keywords in the paragraph
            for keyword in keywords:
                rank += paragraph.count(keyword)

            # Count entities with matching label in paragraph
            if label:
                doc = self.nlp(paragraph)
                rank += len([
                    True
                    for ent in doc.ents
                    if ent.label_ == label
                ])
            ranks.append(rank)

        # Highest rank index
        top_idx = ranks.index(max(ranks))

        return paragraphs[top_idx]

    def find_periods_paragraph(self,  paragraphs: t.Sequence[str]):
        """ Returns the content of the periods paragraph """
        return self.find_paragraph(paragraphs, self.periods_keywords, self.periods_label)

    @staticmethod
    def split_into_paragraphs(text: str) -> t.List[str]:
        return [p.strip() for p in re.split(r'\s*\n\s*|\s*-\s*', text) if p.strip()]

    def parse(self, text: str) -> dict:
        paragraphs = self.split_into_paragraphs(text)

        periods_text = self.find_periods_paragraph(paragraphs)
        periods = self.extract_periods(periods_text)

        contributions_paragraph = self.find_contributions_paragraph(paragraphs)
        amount_min, amount_max = self.extract_amounts(contributions_paragraph)

        return {
            'periods': [
                {'start': p[0].strftime('%b %d'), 'end': p[1].strftime('%b %d')}
                for p in periods
            ],
            'amount_max': amount_max,
            'amount_min': amount_min,
        }