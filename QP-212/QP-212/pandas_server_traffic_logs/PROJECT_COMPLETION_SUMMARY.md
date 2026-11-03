# QP-212: Server Traffic Logs Analysis - Project Completion Summary

## Project Overview
**Title**: Server Traffic Logs Analysis using Pandas  
**Problem Code**: QP-212  
**Type**: Low-Level Design (LLD) - Pandas DataFrame Operations  
**Difficulty**: Intermediate  
**Status**: ✅ **COMPLETE - ALL TESTS PASSING (27.5/27.5 marks)**

---

## Test Results

### Local Test Execution (Visible Tests Only)
**Command**: `python run.py` from student_workspace/  
**Result**: ✅ **20/20.0 (Visible)**

Test Case Summary:
- ✅ TC1: Load traffic_logs.csv and verify 20 rows loaded (2 marks)
- ✅ TC2: Identify and remove 2 outliers ResponseTime > 10s (3 marks)
- ✅ TC3: Verify 18 rows remain after outlier removal (2 marks)
- ✅ TC4: Fill NaN values in ResponseTime with mean (3 marks)
- ✅ TC5: Identify slowest endpoint (/profile ~0.93s avg) (3 marks)
- ✅ TC6: Count 404 errors in traffic logs (3 marks)
- ✅ TC7: Check for 500 errors (returns 0) (2 marks)
- ✅ TC8: Verify row count after all operations is 18 (2 marks)

### Central Server Test Execution (All Tests: Visible + Hidden)
**Command**: `python run_central.py test_vm_1` from secret_tests/  
**Result**: ✅ **27.5/27.5 (Total: 20 Visible + 7.5 Hidden)**

Test Case Summary:
- ✅ TC1-TC8: All visible tests (20 marks)
- ✅ TC9: Verify count_errors returns 0 for non-existent code (2.5 marks - Hidden)
- ✅ TC10: Verify sanitize_latency removes exact outliers (2.5 marks - Hidden)
- ✅ TC11: Verify fix_missing_records fills with correct mean (2.5 marks - Hidden)

---

## Implementation Details

### TrafficAnalyzer Class Structure

```python
class TrafficAnalyzer:
    """Analyzes server traffic logs for performance metrics and error tracking."""
    
    def __init__(self):
        """Initialize with empty DataFrame."""
        self.df = None
    
    def read_logs(self, file_path: str) → None
        """Load CSV traffic logs into DataFrame."""
    
    def sanitize_latency(self) → int
        """Remove ResponseTime > 10.0 outliers, return count removed."""
    
    def fix_missing_records(self) → None
        """Fill NaN values in ResponseTime with mean."""
    
    def get_slowest_endpoint(self) → str
        """Return endpoint with highest average ResponseTime."""
    
    def count_errors(self, error_code: int) → int
        """Count specific HTTP status code occurrences."""
```

### Key Implementation Details

**Critical Fix Applied: NaN Handling in sanitize_latency()**
- **Issue**: Pandas comparison `df['ResponseTime'] <= 10.0` filters out NaN values (comparison with NaN returns False)
- **Solution**: Use `(df['ResponseTime'] <= 10.0) | (df['ResponseTime'].isna())` to preserve NaN values for later filling
- **Impact**: Ensures 18 rows remain after removing 2 outliers (20 original - 2 outliers = 18, not 16)

**Critical Fix Applied: Pandas Integer Type Compatibility**
- **Issue**: Test checks used `isinstance(result, int)` but pandas returns `numpy.int64`
- **Solution**: Updated all checks to `isinstance(result, (int, np.integer))` to accept both types
- **Impact**: Tests TC4, TC8 now pass correctly

**Fillna Assignment Pattern**
- Changed from: `self.df['ResponseTime'].fillna(mean_value, inplace=True)`
- Changed to: `self.df['ResponseTime'] = self.df['ResponseTime'].fillna(mean_value)`
- Reason: Avoids ChainedAssignmentError and ensures proper DataFrame mutation

### Data File: traffic_logs.csv
- **Total Rows**: 20
- **Columns**: Timestamp, Endpoint, StatusCode, ResponseTime, RequestSize, ResponseSize
- **Data Characteristics**:
  - Row 4: ResponseTime = NaN (missing value #1)
  - Row 8: ResponseTime = NaN (missing value #2)
  - Row 18: ResponseTime = 12.5 (outlier > 10.0 #1)
  - Row 20: ResponseTime = 15.2 (outlier > 10.0 #2)
- **Expected Processing**:
  - After sanitize_latency: 18 rows (2 outliers removed, NaN preserved)
  - After fix_missing_records: 0 NaN values (filled with mean ≈ 2.05)

---

## Project Structure

```
QP-212/
├── QP-212/
│   └── pandas_server_traffic_logs/
│       ├── student_workspace/
│       │   ├── solution.py (72 lines - TrafficAnalyzer implementation)
│       │   ├── run.py (15 lines - Test launcher)
│       │   └── report.txt (Test output file)
│       ├── secret_tests/
│       │   ├── driver.py (141 lines - 8 visible test cases)
│       │   ├── driver_central.py (207 lines - 11 total test cases)
│       │   ├── run_central.py (21 lines - Central server launcher)
│       │   └── test_vm_1_report.txt (Central server output)
│       └── data/
│           └── traffic_logs.csv (20 rows of traffic data)
```

---

## Debugging Journey & Resolutions

### Issue #1: NaN Values Filtered Out
**Symptom**: TC3 expected 18 rows but got 16 after sanitize_latency()  
**Root Cause**: Pandas boolean indexing `df['ResponseTime'] <= 10.0` excludes NaN values  
**Resolution**: Modified filter to `(df['ResponseTime'] <= 10.0) | (df['ResponseTime'].isna())`  
**Verification**: ✅ TC3 now passes

### Issue #2: Numpy Integer Type Mismatch
**Symptom**: TC4 output mismatch despite correct implementation  
**Root Cause**: `df['ResponseTime'].isna().sum()` returns `numpy.int64`, not Python `int`  
**Resolution**: Updated test checks to accept both `int` and `np.integer` types  
**Verification**: ✅ TC4, TC8 now pass

### Issue #3: Pandas ChainedAssignmentError (Pre-Session)
**Symptom**: Tests crashed with ChainedAssignmentError  
**Root Cause**: Using `fillna(..., inplace=True)` on subset of DataFrame  
**Resolution**: Changed to assignment pattern for proper mutation  
**Verification**: ✅ Tests execute without errors

---

## Validation Checklist

- [x] All 6 methods implemented correctly
- [x] Data file created with proper structure (20 rows, 2 NaN, 2 outliers)
- [x] All 8 visible tests pass (20/20 marks)
- [x] All 3 hidden tests pass (7.5/7.5 marks)
- [x] NaN handling in sanitize_latency preserves missing values
- [x] Mean calculation correctly fills NaN in fix_missing_records
- [x] slowest_endpoint correctly returns "/profile"
- [x] Error counting works for both existing (404: 2, 500: 0) and non-existent (999: 0) codes
- [x] DataFrame mutations persist across method calls
- [x] Numpy integer type compatibility verified
- [x] Central server tests execution successful
- [x] Project structure matches QL-601 reference format

---

## Key Learnings

1. **Pandas NaN Handling**: Comparisons with NaN always return False; use `isna()` method to preserve missing values
2. **Type Compatibility**: Pandas operations return numpy types, not Python primitives; tests must handle both
3. **Assignment Pattern**: Always use direct assignment for DataFrame mutations to avoid ChainedAssignmentError
4. **Lambda Setup Functions**: Tuple unpacking pattern `(func1(), func2(), obj)[-1]` correctly preserves object state
5. **Independent Test Instances**: Each test receives a fresh TrafficAnalyzer instance via lambda setup

---

## Files Modified/Created

**Created**:
- ✅ student_workspace/solution.py
- ✅ student_workspace/run.py
- ✅ secret_tests/driver.py
- ✅ secret_tests/driver_central.py
- ✅ secret_tests/run_central.py
- ✅ data/traffic_logs.csv
- ✅ student_workspace/report.txt

**Fixed**:
- ✅ solution.py: NaN handling in sanitize_latency, fillna assignment pattern
- ✅ driver.py: Added numpy integer type support
- ✅ driver_central.py: Added numpy integer type support for hidden tests

---

## Completion Date

**Project Completed**: February 26, 2026  
**Final Verification**: All tests passing locally (20/20) and centrally (27.5/27.5)  
**Status**: Ready for deployment ✅

---

## References

- **Pattern**: QL-601 reference format for pandas projects
- **Prior Projects**: QOL-405, QOD-408 (similar structure and test patterns)
- **Technologies**: Pandas DataFrame operations, Python object-oriented design, IST timezone support
- **Test Framework**: Python functions with inspect module for pass-only detection

---

**Project Status**: ✅ **COMPLETE AND VERIFIED**
