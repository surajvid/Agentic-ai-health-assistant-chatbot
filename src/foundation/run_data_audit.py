from src.data.data_loader import DataLoader
from src.foundation.data_audit import DataAuditor


def main():
    loader = DataLoader(data_dir="data")

    df1 = loader.load_file("Health Dataset 1.xlsm")
    df2 = loader.load_file("Health Dataset 2.xlsm")

    dataset_1_audit = DataAuditor.audit_dataset(
        df=df1,
        dataset_name="Health Dataset 1",
        primary_key="Patient_Number",
        grain_keys=["Patient_Number"]
    )

    dataset_2_audit = DataAuditor.audit_dataset(
        df=df2,
        dataset_name="Health Dataset 2",
        primary_key=None,
        grain_keys=["Patient_Number", "Day_Number"]
    )

    key_comparison = DataAuditor.compare_dataset_keys(
        df1=df1,
        df2=df2,
        key="Patient_Number"
    )

    report_text = DataAuditor.build_audit_text_report(
        dataset_1_audit=dataset_1_audit,
        dataset_2_audit=dataset_2_audit,
        key_comparison=key_comparison
    )

    print(report_text)

    print("\nDATASET 1 COLUMNS:")
    print(dataset_1_audit["columns"])

    print("\nDATASET 2 COLUMNS:")
    print(dataset_2_audit["columns"])

    print("\nDATASET 1 MISSING SUMMARY:")
    print(dataset_1_audit["missing_summary"])

    print("\nDATASET 2 MISSING SUMMARY:")
    print(dataset_2_audit["missing_summary"])


if __name__ == "__main__":
    main()