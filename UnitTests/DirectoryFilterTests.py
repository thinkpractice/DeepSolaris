import unittest
from DirectoryFilter import DirectoryFilter


class DirectoryFilterTests(unittest.TestCase):
    def test_rgb_returns_rgb_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013.tiff",
                          "00024a4c-53fe-4d74-838b-20b8ee7f4777_rgb_2013.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013.tiff"],
                         DirectoryFilter(r"TestData/2013").rgb.images.files)

    def test_rgb_mask_returns_mask_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013_mask.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013_mask.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013_mask.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_rgb_2013_mask.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013_mask.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013_mask.tiff"],
                         DirectoryFilter(r"TestData/2013").rgb.masks.files)

    def test_rgb_masked_returns_masked_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013_masked.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013_masked.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013_masked.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_rgb_2013_masked.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013_masked.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013_masked.tiff"],
                         DirectoryFilter(r"TestData/2013").rgb.masked.files)


    def test_ir_returns_ir_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_ir_2013.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_ir_2013.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_ir_2013.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_ir_2013.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_ir_2013.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_ir_2013.tiff"],
                         DirectoryFilter(r"TestData/2013").ir.images.files)

    def test_ir_mask_returns_mask_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_ir_2013_mask.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_ir_2013_mask.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_ir_2013_mask.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_ir_2013_mask.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_ir_2013_mask.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_ir_2013_mask.tiff"],
                         DirectoryFilter(r"TestData/2013").ir.masks.files)

    def test_ir_masked_returns_masked_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_ir_2013_masked.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_ir_2013_masked.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_ir_2013_masked.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_ir_2013_masked.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_ir_2013_masked.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_ir_2013_masked.tiff"],
                         DirectoryFilter(r"TestData/2013").ir.masked.files)

    def test_all_image_files_returns_image_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_ir_2013.tiff",
                          "0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_ir_2013.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_ir_2013.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_ir_2013.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_rgb_2013.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_ir_2013.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_ir_2013.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013.tiff"],
                         DirectoryFilter(r"TestData/2013").all.images.files)

    def test_all_mask_files_returns_mask_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_ir_2013_mask.tiff",
                          "0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013_mask.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_ir_2013_mask.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013_mask.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_ir_2013_mask.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013_mask.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_ir_2013_mask.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_rgb_2013_mask.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_ir_2013_mask.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013_mask.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_ir_2013_mask.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013_mask.tiff"],
                         DirectoryFilter(r"TestData/2013").all.masks.files)

    def test_all_masked_files_returns_masked_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_ir_2013_masked.tiff",
                          "0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013_masked.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_ir_2013_masked.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013_masked.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_ir_2013_masked.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013_masked.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_ir_2013_masked.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_rgb_2013_masked.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_ir_2013_masked.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013_masked.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_ir_2013_masked.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013_masked.tiff"],
                         DirectoryFilter(r"TestData/2013").all.masked.files)

    def test_dir_returns_subdir_rgb_files(self):
        self.assertEqual(["0000085b-6f4a-475a-b800-9ed7619e8a67_rgb_2013.tiff",
                          "00001900-3f87-4a57-8e1a-8fbdf3127213_rgb_2013.tiff",
                          "00023872-f873-4889-9b80-113677b9e86a_rgb_2013.tiff",
                          "00024a4c-54fe-4d74-838b-20b8ee7f4777_rgb_2013.tiff",
                          "00031d78-fd98-4371-ac7f-8f2ddf487021_rgb_2013.tiff",
                          "00036fd4-14a1-49a4-ae79-feaa26847d61_rgb_2013.tiff"],
                         DirectoryFilter(r"TestData").dir("2013").rgb.images.files)

    def test_not_existing_dir_returns_empty_list(self):
        self.assertEqual([], DirectoryFilter(r"TestData").dir("1900").rgb.images.files)



if __name__ == '__main__':
    unittest.main()
