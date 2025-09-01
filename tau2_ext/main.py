"""Main analysis script for τ²-bench metrics."""
import argparse
import pandas as pd
from pathlib import Path
from typing import List, Optional

from tau2_ext.data_processing.data_preparer import DataPreparer
from metrics_calculator import MetricsCalculator, MetricsVisualizer


def run_analysis(
    simulation_files: List[str],
    output_dir: Optional[str] = None
) -> pd.DataFrame:
    """Run comprehensive analysis on simulation files."""
    
    print(f"🔍 Analyzing {len(simulation_files)} simulation files...")
    
    data_preparer = DataPreparer()
    df = data_preparer.prepare_multiple_simulation_files(simulation_files)
    
    if df.empty:
        print("❌ No conversation data found")
        return df
    
    print(f"✅ Prepared {len(df)} conversations")
    print(f"📊 Success rate: {df['success'].mean():.2%}")
    print(f"📏 Average plan length: {df['exp_plan_len'].mean():.1f}")
    
    # Calculate metrics
    calculator = MetricsCalculator()
    results = calculator.calculate_all_metrics(df)
    
    # Print summary
    print(f"\n📈 METRICS SUMMARY:")
    print(f"Complexity-weighted pass@1: {results.complexity_weighted_pass1:.3f}")
    
    print(f"\n🔧 Per-Tool Analysis:")
    for _, row in results.per_tool_prf.iterrows():
        print(f"  {row['tool']:30s}: P={row['precision']:.2f}, R={row['recall']:.2f}, F1={row['f1']:.2f}")
    
    print(f"\n🎯 Tool Criticality (Top 5):")
    tci_sorted = results.tool_criticality.dropna(subset=["TCI"]).sort_values("TCI", ascending=False)
    for _, row in tci_sorted.head(5).iterrows():
        print(f"  {row['tool']:30s}: TCI={row['TCI']:.3f}")
    
    print(f"\n📊 Complexity Buckets:")
    for _, row in results.bucket_pass1.iterrows():
        bucket_name = str(row.iloc[0])
        pass_rate = row['pass@1']
        print(f"  {bucket_name:10s}: {pass_rate:.2%}")
    
    # Create visualizations
    visualizer = MetricsVisualizer()
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save results to CSV
        results.per_tool_prf.to_csv(output_path / "per_tool_prf.csv", index=False)
        results.tool_criticality.to_csv(output_path / "tool_criticality.csv", index=False)
        results.sequence_compliance.to_csv(output_path / "sequence_compliance.csv", index=False)
        results.bucket_pass1.to_csv(output_path / "bucket_pass1.csv", index=False)
        
        # Save summary
        with open(output_path / "summary.txt", "w") as f:
            f.write(f"Analysis Summary\n")
            f.write(f"================\n")
            f.write(f"Files analyzed: {len(simulation_files)}\n")
            f.write(f"Conversations: {len(df)}\n")
            f.write(f"Success rate: {df['success'].mean():.2%}\n")
            f.write(f"Complexity-weighted pass@1: {results.complexity_weighted_pass1:.3f}\n")
            f.write(f"Domains: {', '.join(df['domain'].unique())}\n")
        
        # Create domain-separated plots
        visualizer.plot_all_metrics_by_domain(results, df, str(output_path))
    else:
        # Just show plots
        visualizer.plot_all_metrics_by_domain(results, df)
    
    return df


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Analyze τ²-bench simulation results")
    parser.add_argument("--input-dir", type=str, required=True,
                       help="Input directory containing simulation JSON files")
    parser.add_argument("--output-dir", type=str, help="Output directory for results")
    parser.add_argument("--tau2-path", type=str, default="/Users/AdminDK/code/tau2-bench", 
                       help="Path to τ²-bench installation")
    
    args = parser.parse_args()
    
    # Get all simulation files from the input directory
    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return
    
    # Find all JSON files in the input directory
    simulation_files = list(input_dir.glob("*.json"))
    
    if not simulation_files:
        print(f"❌ No JSON files found in input directory: {input_dir}")
        return
    
    print(f"📁 Found {len(simulation_files)} simulation files in {input_dir}")
    for f in simulation_files[:5]:  # Show first 5
        print(f"  {f.name}")
    if len(simulation_files) > 5:
        print(f"  ... and {len(simulation_files) - 5} more")
    
    # Run analysis
    df = run_analysis(simulation_files, args.output_dir)
    
    if not df.empty:
        print(f"\n✅ Analysis complete!")
        if args.output_dir:
            print(f"📁 Results saved to: {args.output_dir}")


if __name__ == "__main__":
    main()
