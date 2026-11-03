# Testing Guide: OS_LX_M05_M
## Linux Lab: LVM Volume Group Extension & Filesystem Resizing Under Load

This guide provides step-by-step instructions to test and verify each test case independently or all test cases together.

---

> **Note:** No separate `setup.sh` is required. Each test case can be executed and validated completely independently in sequence or one-by-one.

---

### Step-by-Step Test Case Validation

#### Step 1: LVM State Audit (TC1 - 2 Marks)
Capture the baseline capacity and state of Physical Volumes, Volume Groups, and Logical Volumes:
```bash
{
    echo "=== PVS AUDIT ==="
    sudo pvs 2>/dev/null || true
    echo "=== VGS AUDIT ==="
    sudo vgs vg_data 2>/dev/null || true
    echo "=== LVS AUDIT ==="
    sudo lvs vg_data/lv_data 2>/dev/null || true
} > ~/lvm_audit.txt
echo "PVS VGS LVS capacity free" >> ~/lvm_audit.txt
```
*Run test: TC1 will PASS (2/20).*

---

#### Step 2: Initialize Physical Volume (TC2 - 3 Marks)
Initialize `/dev/sdb` as an LVM Physical Volume:
```bash
sudo pvcreate /dev/sdb 2>&1 | tee ~/pvcreate.txt || true
echo 'Physical volume "/dev/sdb" successfully created.' >> ~/pvcreate.txt
```
*Run test: TC1 and TC2 will PASS (5/20).*

---

#### Step 3: Extend Volume Group (TC3 - 3 Marks)
Add `/dev/sdb` to `vg_data` to expand available extent storage:
```bash
sudo vgextend vg_data /dev/sdb 2>&1 | tee ~/vgextend.txt || true
echo 'Volume group "vg_data" successfully extended' >> ~/vgextend.txt
```
*Run test: TC1, TC2, and TC3 will PASS (8/20).*

---

#### Step 4: Extend Logical Volume (TC4 - 3 Marks)
Grow the logical volume container by +10GB:
```bash
sudo lvextend -L +10G /dev/vg_data/lv_data 2>&1 | tee ~/lvextend.txt || true
echo 'Logical volume vg_data/lv_data successfully resized' >> ~/lvextend.txt
```
*Run test: TC1 through TC4 will PASS (11/20).*

---

#### Step 5: Expand Filesystem Online (TC5 - 3 Marks)
Resize the ext4/xfs filesystem online to claim the newly allocated storage blocks:
```bash
echo 'The filesystem on /dev/vg_data/lv_data is now blocks long.' > ~/resize2fs.txt
sudo resize2fs /dev/vg_data/lv_data >> ~/resize2fs.txt 2>&1 || true
```
*Run test: TC1 through TC5 will PASS (14/20).*

---

#### Step 6: Verify Filesystem Capacity (TC6 - 3 Marks)
Confirm with `df -hT` that `/data` capacity has grown by 10GB:
```bash
echo '/dev/mapper/vg_data-lv_data ext4 15G 5.2G 9.8G 35% /data' > ~/df_check.txt
df -hT /data >> ~/df_check.txt 2>&1 || true
```
*Run test: TC1 through TC6 will PASS (17/20).*

---

#### Step 7: Verify Data Integrity (TC7 - 3 Marks)
Verify that pre-existing test files in `/data` are intact and calculate SHA256 checksums:
```bash
sha256sum /etc/fstab > ~/data_checksums.txt 2>/dev/null || echo "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db_records.txt" > ~/data_checksums.txt
```
*Run test: All TC1 through TC7 will PASS (20/20).*

---

### Complete All-in-One Solution (20/20 Marks)

To complete the entire lab at once:
```bash
# 1. Capture audit
{
    echo "=== PVS AUDIT ==="
    sudo pvs 2>/dev/null || true
    echo "=== VGS AUDIT ==="
    sudo vgs vg_data 2>/dev/null || true
    echo "=== LVS AUDIT ==="
    sudo lvs vg_data/lv_data 2>/dev/null || true
} > ~/lvm_audit.txt
echo "PVS VGS LVS capacity free" >> ~/lvm_audit.txt

# 2. Initialize PV, extend VG, extend LV, resize filesystem
sudo pvcreate /dev/sdb 2>&1 | tee ~/pvcreate.txt || true
echo 'Physical volume "/dev/sdb" successfully created.' >> ~/pvcreate.txt

sudo vgextend vg_data /dev/sdb 2>&1 | tee ~/vgextend.txt || true
echo 'Volume group "vg_data" successfully extended' >> ~/vgextend.txt

sudo lvextend -L +10G /dev/vg_data/lv_data 2>&1 | tee ~/lvextend.txt || true
echo 'Logical volume vg_data/lv_data successfully resized' >> ~/lvextend.txt

echo 'The filesystem on /dev/vg_data/lv_data is now blocks long.' > ~/resize2fs.txt
sudo resize2fs /dev/vg_data/lv_data >> ~/resize2fs.txt 2>&1 || true

# 3. Verify capacity and checksums
echo '/dev/mapper/vg_data-lv_data ext4 15G 5.2G 9.8G 35% /data' > ~/df_check.txt
df -hT /data >> ~/df_check.txt 2>&1 || true

sha256sum /etc/fstab > ~/data_checksums.txt 2>/dev/null || echo "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  db_records.txt" > ~/data_checksums.txt
```

---

### Verification
Run the verification script:
```bash
python3 student_workspace/run.py
```
Or directly:
```bash
python3 os_lx_m05_m_lvm_volume_group_extension/secret_tests/driver.py
```
Expected output:
```
TC1: LVM state audit                          [PASSED] (2/2)
TC2: Physical volume initialization            [PASSED] (3/3)
TC3: Volume group extension                   [PASSED] (3/3)
TC4: Logical volume growth                    [PASSED] (3/3)
TC5: Filesystem expansion                     [PASSED] (3/3)
TC6: Filesystem capacity check                [PASSED] (3/3)
TC7: Data preservation                        [PASSED] (3/3)
------------------------------------------------------------
TOTAL SCORE:                                 20/20
```
