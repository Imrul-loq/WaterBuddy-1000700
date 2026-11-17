"""Run with python -m unittest -v. No extra testing dependency needed."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
from app import AGE_GOALS, calculate_progress, parse_amount, reaction

class LogicTests(unittest.TestCase):
    def test_invalid_amounts(self):
        for value in ('', 'abc', '-1', '0', '2001', '1.5', 'nan', 'inf'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_amount(value)
        self.assertEqual(parse_amount(' 350 '), 350)

    def test_calculations_and_milestones(self):
        for total, expected in [(0,'calm'),(499,'calm'),(500,'smile'),
                                (750,'wave'),(1000,'celebrate'),(1250,'celebrate')]:
            remaining, pct, fill = calculate_progress(total,1000)
            self.assertEqual(remaining,max(1000-total,0))
            self.assertEqual(pct,total/10)
            self.assertLessEqual(fill,100)
            self.assertEqual(reaction(pct)[0],expected)
        with self.assertRaises(ValueError):
            calculate_progress(100,0)

class InteractionTests(unittest.TestCase):
    def setUp(self):
        self.at = AppTest.from_file(str(Path(__file__).with_name('app.py'))).run()
    def button(self,label):
        return next(b for b in self.at.button if b.label == label)
    def test_age_goals(self):
        for group,goal in AGE_GOALS.items():
            self.at.selectbox[0].select(group).run()
            self.assertEqual(self.at.session_state['goal_ml'],goal)
            self.assertFalse(self.at.exception)
    def test_logging_goal_change_reset_and_isolation(self):
        self.button('+250 ml').click().run()
        self.button('+250 ml').click().run()
        self.assertEqual(self.at.session_state['total_ml'],500)
        self.at.text_input[0].input('750')
        self.button('Add water').click().run()
        self.assertEqual(self.at.session_state['total_ml'],1250)
        for invalid in ('0','-100','abc','', '2001'):
            self.at.text_input[0].input(invalid)
            self.button('Add water').click().run()
            self.assertEqual(self.at.session_state['total_ml'],1250)
            self.assertTrue(self.at.error)
        self.at.number_input[0].set_value(1000).run()
        self.assertEqual(self.at.metric[1].value,'0 ml')
        self.assertTrue(any('125.0' in item.value for item in self.at.markdown))
        self.button('New Day').click().run()
        self.button('Cancel').click().run()
        self.assertEqual(self.at.session_state['total_ml'],1250)
        self.button('New Day').click().run()
        self.button('Confirm new day').click().run()
        self.assertEqual(self.at.session_state['total_ml'],0)
        self.assertEqual(self.at.session_state['goal_ml'],1000)
        self.assertEqual(self.at.session_state['entries'],[])
        self.assertFalse(self.at.exception)
        fresh=AppTest.from_file(str(Path(__file__).with_name('app.py'))).run()
        self.assertEqual(fresh.session_state['total_ml'],0)
        self.assertEqual(fresh.session_state['goal_ml'],2250)
    def test_live_milestones_and_no_duplicate_celebration(self):
        self.at.number_input[0].set_value(1000).run()
        for count in range(1,6):
            self.button('+250 ml').click().run()
            total=count*250
            self.assertEqual(self.at.metric[0].value,f'{total:,} ml')
            self.assertEqual(self.at.metric[1].value,f'{max(1000-total,0):,} ml')
            expected=reaction(total/10)[1]
            self.assertTrue(any(expected in m.value for m in self.at.markdown))
        self.assertEqual(self.at.session_state['celebrated'],{50,75,100})
        self.assertNotIn('milestone',self.at.success[0].value)
        self.assertFalse(self.at.exception)

if __name__ == '__main__':
    unittest.main()
