import datetime

from django.test import TestCase

from .parser import Parser


class ParserTest(TestCase):
    def test_dates_distance(self):
        self.assertEqual(
            Parser().calculate_dates_distance(
                date_since=datetime.date(2000, 1, 5),
                date_till=datetime.date(2000, 1, 6),
            ),
            1
        )
        self.assertEqual(
            Parser().calculate_dates_distance(
                date_since=datetime.date(2000, 12, 31),
                date_till=datetime.date(2000, 1, 1),
            ),
            1
        )

    def test_extract_amounts(self):
        self.assertEqual(
            Parser().extract_amounts('40%, $5000'),
            ('', '40.0% or $5000.0')
        )

    def test_extract_periods(self):
        self.assertEqual(
            Parser().extract_periods('January 1, April 1, July 1 and October 1'),
            [
                [datetime.datetime(2004, 1, 1, 0, 0), datetime.datetime(2004, 3, 31, 0, 0)],
                [datetime.datetime(2004, 4, 1, 0, 0), datetime.datetime(2004, 6, 30, 0, 0)],
                [datetime.datetime(2004, 7, 1, 0, 0), datetime.datetime(2004, 9, 30, 0, 0)],
                [datetime.datetime(2004, 10, 1, 0, 0), datetime.datetime(2003, 12, 31, 0, 0)],
            ]
        )

    def test_parse(self):
        self.assertEqual(
            Parser().parse(
                '    - Initial Contribution Periods. Subject to the following paragraph (b), '
                'the Plan shall be implemented by a series of consecutive Contribution Periods commencing '
                'on January 1 and July 1 each year and ending on the following June 30 and December 31, respectively. '
                'The first Contribution Period under this Plan shall commence on July 1, 2010, and shall end '
                'on December 31, 2010. The Plan shall continue until terminated '
                'in accordance with Section 13 or Section 19.\n'
                '    - Changes. The Committee shall have the power to change the duration and/or frequency of '
                'Contribution Periods with respect to future purchases of Shares, without shareholder approval, '
                'if such change is announced to all Employees who are eligible under Section 3 at least '
                'five Business Days before the Commencement Date of the first Contribution Period to be '
                'affected by the change; provided, however, that no Contribution Period shall exceed 27 months.\n'
                '    - Contribution Amounts. Subject to the limitations of Sections 3(b) and 11, '
                'a Participant shall elect to have Contributions made as payroll deductions on each payday '
                'during the Contribution Period in any percentage of his or her Compensation that is '
                'not less than 1% and not more than 15% (or such other maximum percentage as the Committee '
                'may establish from time to time before any Commencement Date) of such Participant’s Compensation '
                'on each payday during the Contribution Period. Contribution amounts shall be withheld '
                'in whole percentages only.\n'
            ),
            {
                'periods': [
                    {'start': 'Jan 01', 'end': 'Jun 30'},
                    {'start': 'Jul 01', 'end': 'Dec 31'},
                ],
                'amount_max': '15.0%',
                'amount_min': '1.0%',
            }
        )
