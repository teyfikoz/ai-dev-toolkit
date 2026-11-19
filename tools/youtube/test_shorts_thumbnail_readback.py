import unittest
from unittest.mock import MagicMock,patch
from PIL import Image,ImageDraw
from shorts_thumbnail_readback import compare,verify

class PortraitVerification(unittest.TestCase):
    def image(self):
        image=Image.new('RGB',(360,640),'#101125');draw=ImageDraw.Draw(image)
        draw.ellipse((60,190,300,430),outline='white',width=8);draw.rectangle((100,80,260,110),fill='#89dfcc');return image
    def test_scaled_jpeg_same_cover_matches(self):
        source=self.image();self.assertTrue(compare(source,source.resize((608,1080)))['match'])
    def test_wrong_landscape_crop_is_not_accepted(self):
        self.assertEqual(compare(self.image(),Image.new('RGB',(640,480),'#101125'))['reason'],'NOT_PORTRAIT_9_16')
    def test_blank_portrait_is_not_accepted(self):
        self.assertFalse(compare(self.image(),Image.new('RGB',(608,1080),'#101125'))['match'])
    def test_landscape_authoring_source_is_not_accepted(self):
        self.assertEqual(compare(Image.new('RGB',(1920,1080)),self.image())['reason'],'EXPECTED_COVER_NOT_PORTRAIT_9_16')
    def test_missing_portrait_resource_never_fetches_legacy_thumbnail(self):
        y=MagicMock();y.videos.return_value.list.return_value.execute.return_value={'items':[{'snippet':{'thumbnails':{'maxres':{'url':'https://i.ytimg.com/legacy.jpg'}}}}]}
        with patch('shorts_thumbnail_readback.urllib.request.urlopen') as network:
            result=verify(y,'example','unused.jpg','unused')
        self.assertFalse(result['match']);network.assert_not_called()
    def test_untrusted_host_is_rejected_before_network(self):
        y=MagicMock();y.videos.return_value.list.return_value.execute.return_value={'items':[{'snippet':{'thumbnails':{'shortsAspectRatio':{'url':'https://untrusted.invalid/image.jpg'}}}}]}
        with patch('shorts_thumbnail_readback.urllib.request.urlopen') as network:
            with self.assertRaisesRegex(ValueError,'UNTRUSTED_THUMBNAIL_HOST'):verify(y,'example','unused.jpg','unused')
        network.assert_not_called()
if __name__=='__main__':unittest.main()
