import unittest

from calculator import calculate_mixed_bed, calculate_ro


class TestROCalculator(unittest.TestCase):
    def test_calculate_ro(self):
        result = calculate_ro(
            feed_flow_m3h=10,
            recovery_percent=75,
            feed_conductivity_us_cm=500,
            salt_rejection_percent=98,
        )
        self.assertAlmostEqual(result.permeate_flow_m3h, 7.5)
        self.assertAlmostEqual(result.concentrate_flow_m3h, 2.5)
        self.assertAlmostEqual(result.salt_passage_percent, 2)
        self.assertAlmostEqual(result.permeate_conductivity_us_cm, 10)


class TestMixedBedCalculator(unittest.TestCase):
    def test_calculate_mixed_bed(self):
        result = calculate_mixed_bed(
            flow_m3h=5,
            runtime_hours=8,
            influent_conductivity_us_cm=30,
            effluent_conductivity_us_cm=1,
            resin_capacity_kg_tds_per_l=0.08,
        )
        self.assertAlmostEqual(result.removed_tds_mg_l, 15.95)
        self.assertAlmostEqual(result.total_removed_tds_kg, 0.638)
        self.assertAlmostEqual(result.required_resin_volume_l, 7.975)


if __name__ == "__main__":
    unittest.main()
