"""Calculator helper for Reverse Osmosis (RO) and Mixed Bed systems."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class ROResult:
    permeate_flow_m3h: float
    concentrate_flow_m3h: float
    salt_rejection_percent: float
    salt_passage_percent: float
    permeate_conductivity_us_cm: float


@dataclass(frozen=True)
class MixedBedResult:
    removed_tds_mg_l: float
    total_removed_tds_kg: float
    required_resin_volume_l: float


def calculate_ro(
    feed_flow_m3h: float,
    recovery_percent: float,
    feed_conductivity_us_cm: float,
    salt_rejection_percent: float,
) -> ROResult:
    if feed_flow_m3h <= 0:
        raise ValueError("feed_flow_m3h must be greater than 0")
    if not 0 < recovery_percent < 100:
        raise ValueError("recovery_percent must be between 0 and 100")
    if feed_conductivity_us_cm < 0:
        raise ValueError("feed_conductivity_us_cm must be non-negative")
    if not 0 <= salt_rejection_percent <= 100:
        raise ValueError("salt_rejection_percent must be between 0 and 100")

    permeate_flow = feed_flow_m3h * (recovery_percent / 100)
    concentrate_flow = feed_flow_m3h - permeate_flow
    salt_passage_percent = 100 - salt_rejection_percent
    permeate_conductivity = feed_conductivity_us_cm * (salt_passage_percent / 100)

    return ROResult(
        permeate_flow_m3h=permeate_flow,
        concentrate_flow_m3h=concentrate_flow,
        salt_rejection_percent=salt_rejection_percent,
        salt_passage_percent=salt_passage_percent,
        permeate_conductivity_us_cm=permeate_conductivity,
    )


def calculate_mixed_bed(
    flow_m3h: float,
    runtime_hours: float,
    influent_conductivity_us_cm: float,
    effluent_conductivity_us_cm: float,
    resin_capacity_kg_tds_per_l: float,
    conductivity_to_tds_factor: float = 0.55,
) -> MixedBedResult:
    if flow_m3h <= 0:
        raise ValueError("flow_m3h must be greater than 0")
    if runtime_hours <= 0:
        raise ValueError("runtime_hours must be greater than 0")
    if influent_conductivity_us_cm < 0 or effluent_conductivity_us_cm < 0:
        raise ValueError("conductivity values must be non-negative")
    if resin_capacity_kg_tds_per_l <= 0:
        raise ValueError("resin_capacity_kg_tds_per_l must be greater than 0")
    if conductivity_to_tds_factor <= 0:
        raise ValueError("conductivity_to_tds_factor must be greater than 0")

    removed_tds_mg_l = max(
        influent_conductivity_us_cm - effluent_conductivity_us_cm,
        0,
    ) * conductivity_to_tds_factor

    total_volume_l = flow_m3h * 1000 * runtime_hours
    total_removed_tds_kg = (removed_tds_mg_l * total_volume_l) / 1_000_000
    required_resin_volume_l = total_removed_tds_kg / resin_capacity_kg_tds_per_l

    return MixedBedResult(
        removed_tds_mg_l=removed_tds_mg_l,
        total_removed_tds_kg=total_removed_tds_kg,
        required_resin_volume_l=required_resin_volume_l,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="RO and Mixed Bed calculation helper",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    ro = subparsers.add_parser("ro", help="Calculate Reverse Osmosis performance")
    ro.add_argument("--feed-flow-m3h", type=float, required=True)
    ro.add_argument("--recovery-percent", type=float, required=True)
    ro.add_argument("--feed-conductivity-us-cm", type=float, required=True)
    ro.add_argument("--salt-rejection-percent", type=float, required=True)

    mixed_bed = subparsers.add_parser("mixed-bed", help="Calculate Mixed Bed resin requirement")
    mixed_bed.add_argument("--flow-m3h", type=float, required=True)
    mixed_bed.add_argument("--runtime-hours", type=float, required=True)
    mixed_bed.add_argument("--influent-conductivity-us-cm", type=float, required=True)
    mixed_bed.add_argument("--effluent-conductivity-us-cm", type=float, required=True)
    mixed_bed.add_argument("--resin-capacity-kg-tds-per-l", type=float, required=True)
    mixed_bed.add_argument("--conductivity-to-tds-factor", type=float, default=0.55)

    return parser


def main() -> None:
    args = _build_parser().parse_args()

    if args.command == "ro":
        result = calculate_ro(
            feed_flow_m3h=args.feed_flow_m3h,
            recovery_percent=args.recovery_percent,
            feed_conductivity_us_cm=args.feed_conductivity_us_cm,
            salt_rejection_percent=args.salt_rejection_percent,
        )
        print(f"Permeate Flow (m3/h): {result.permeate_flow_m3h:.3f}")
        print(f"Concentrate Flow (m3/h): {result.concentrate_flow_m3h:.3f}")
        print(f"Salt Rejection (%): {result.salt_rejection_percent:.2f}")
        print(f"Salt Passage (%): {result.salt_passage_percent:.2f}")
        print(f"Estimated Permeate Conductivity (uS/cm): {result.permeate_conductivity_us_cm:.3f}")
        return

    result = calculate_mixed_bed(
        flow_m3h=args.flow_m3h,
        runtime_hours=args.runtime_hours,
        influent_conductivity_us_cm=args.influent_conductivity_us_cm,
        effluent_conductivity_us_cm=args.effluent_conductivity_us_cm,
        resin_capacity_kg_tds_per_l=args.resin_capacity_kg_tds_per_l,
        conductivity_to_tds_factor=args.conductivity_to_tds_factor,
    )
    print(f"Removed TDS (mg/L): {result.removed_tds_mg_l:.3f}")
    print(f"Total TDS Removed (kg): {result.total_removed_tds_kg:.3f}")
    print(f"Required Resin Volume (L): {result.required_resin_volume_l:.3f}")


if __name__ == "__main__":
    main()
