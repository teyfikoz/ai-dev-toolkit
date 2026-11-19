"""Verify the actual 9:16 Shorts CDN thumbnail, not a cropped 16:9 proxy."""
import hashlib,io,urllib.request,urllib.parse
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps

def phash(im):
    a=np.asarray(ImageOps.grayscale(ImageOps.fit(im,(32,32))),dtype=float)
    n=np.arange(32);k=n[:,None];c=np.cos(np.pi*(2*n+1)*k/64);low=(c@a@c.T)[:8,:8]
    return low>np.median(low.flat[1:])
def compare(expected,actual):
    if abs(expected.width/expected.height-9/16)>.015:return {'match':False,'reason':'EXPECTED_COVER_NOT_PORTRAIT_9_16'}
    ratio=actual.width/actual.height
    if abs(ratio-9/16)>.015:return {'match':False,'reason':'NOT_PORTRAIT_9_16'}
    distance=int(np.count_nonzero(phash(expected)!=phash(actual)))
    return {'match':distance<=8,'perceptual_hash_distance':distance,'reason':'MATCH' if distance<=8 else 'PIXEL_CONTENT_MISMATCH'}
def verify(y,video_id,expected,folder):
    rows=y.videos().list(part='snippet,contentDetails',id=video_id).execute().get('items',[])
    if len(rows)!=1:return {'match':False,'reason':'VIDEO_MISSING'}
    thumb=rows[0]['snippet'].get('thumbnails',{}).get('shortsAspectRatio')
    if not thumb:return {'match':False,'reason':'SHORTS_ASPECT_RATIO_NOT_AVAILABLE'}
    url=thumb['url'];p=urllib.parse.urlparse(url)
    if p.scheme!='https' or p.hostname not in ('i.ytimg.com','i9.ytimg.com','img.youtube.com'):raise ValueError('UNTRUSTED_THUMBNAIL_HOST')
    raw=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Selfix-thumbnail-QA/1.0','Cache-Control':'no-cache'}),timeout=25).read()
    actual=Image.open(io.BytesIO(raw)).convert('RGB');source=Image.open(expected).convert('RGB')
    result=compare(source,actual);dest=Path(folder)/f'{video_id}_shorts_portrait_verified.jpg';dest.write_bytes(raw)
    return {**result,'url':url,'resolution':list(actual.size),'file':str(dest),'download_sha256':hashlib.sha256(raw).hexdigest(),'has_custom_thumbnail':rows[0].get('contentDetails',{}).get('hasCustomThumbnail'),'thumbnail_resource':'shortsAspectRatio'}
