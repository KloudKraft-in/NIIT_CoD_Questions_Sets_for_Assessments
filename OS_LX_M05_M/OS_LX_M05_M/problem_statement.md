# Linux Lab: LVM Volume Group Extension & Filesystem Resizing Under Load (Local VM)

Duration : 90 Min.

## Scenario

A production database logical volume /dev/vg_data/lv_data mounted on /data is at 95% capacity. A new physical disk block device /dev/sdb (20GB) has been attached. You must initialize the physical volume, extend the existing volume group, grow the logical volume by 10GB, and expand the filesystem online with zero data loss and zero downtime.

## Task Objectives

Perform the following actions inside your home directory (`~`) of the local Linux system:

### 1. Inspect current LVM configuration

- Inspect current LVM configuration using `pvs`, `vgs`, and `lvs`.
- Record the initial baseline LVM capacity audit into `~/lvm_audit.txt`.

### 2. Initialize block device /dev/sdb

- Initialize block device `/dev/sdb` as an LVM Physical Volume using `pvcreate /dev/sdb`.
- Record initialization verification into `~/pvcreate.txt`.

### 3. Extend Volume Group vg_data

- Extend Volume Group `vg_data` with `/dev/sdb` using `vgextend vg_data /dev/sdb`.
- Record volume group extension verification into `~/vgextend.txt`.

### 4. Extend Logical Volume lv_data

- Extend Logical Volume `lv_data` by +10G using `lvextend -L +10G /dev/vg_data/lv_data`.
- Record logical volume resize confirmation into `~/lvextend.txt`.

### 5. Expand the active filesystem

- Expand the active filesystem online using `resize2fs /dev/vg_data/lv_data` (or `xfs_growfs /data`).
- Record filesystem block expansion output into `~/resize2fs.txt`.

### 6. Verify that df -hT

- Verify that `df -hT /data` reflects the expanded 15GB capacity.
- Record the filesystem capacity check into `~/df_check.txt`.

### 7. Confirm data integrity of

- Confirm data integrity of test files in `/data` using SHA256 checksums.
- Record the data integrity verification checksums into `~/data_checksums.txt`.

## Verification

Once you have performed the tasks, you can run the verification script to check your progress and receive your score.

## Grading Criteria

Your performance will be evaluated based on the following test cases:

| Test Case | Requirement | Marks |
| --------- | ----------- | ----- |
| **TC1** | LVM state audit: initial pvs, vgs, lvs capacity recorded before extension | 2 Marks |
| **TC2** | Physical volume initialization: pvcreate /dev/sdb succeeds | 3 Marks |
| **TC3** | Volume group extension: vgextend vg_data /dev/sdb increases VG free extent size | 3 Marks |
| **TC4** | Logical volume growth: lvextend -L +10G expands logical volume container | 3 Marks |
| **TC5** | Filesystem expansion: resize2fs / xfs_growfs extends filesystem blocks online | 3 Marks |
| **TC6** | Filesystem capacity check: df -hT confirms /data capacity increased by exactly 10GB | 3 Marks |
| **TC7** | Data preservation: sha256 checksum of existing test files in /data remains identical | 3 Marks |

**Total Score: 20 Marks**
