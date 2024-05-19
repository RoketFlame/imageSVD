# imageSVD

Utility for comressing/decompressing images using SVD.

This utility takes a BMP image as input and compresses it using SVD for each of the RGB channels.
Examples of using the utility, as well as the structure of compressed images are presented below.

## Usage

```bash
cdisvd compress --out-file compressed --method power-iterations input-file.bmp
cdisvd decompress --out-file decompressed.bmp input-file
```

## Commads and arguments
```bash
cdisvd --help
cdisvd compress --help
cdisvd decompress --help
```

## Compressed format

The compressed image has the following structure.

| Part   | Size bytes | Desc                                                     |
|--------|------------|----------------------------------------------------------|
| Header | 16         | Contains general information about the compressed image. |
| Body   | Variable   | Contains an image using matrices.                        |

### Header

| Offset hex | Size bytes | Name      | Type   | Desc                                                   |
|------------|------------|-----------|--------|--------------------------------------------------------|
| 00         | 4          | signature | uint32 | Signature of compressed file, must be "BOOB" in ASCII. |
| 04         | 4          | Width     | uint32 | Width of image in pixels.                              |
| 08         | 4          | Height    | uint32 | Height of image in pixels.                             |
| 0C         | 4          | K         | uint32 | One side size of matrix, computes automaticly.         |

### Body

There are tree part for each RBG's channel. 
All values are written sequentially, without any alignments or separators.

| Name | Size bytes     | Type    | Description                                 |
|------|----------------|---------|---------------------------------------------|
| U    | 4 * width * k  | float32 | Matrix containing of left singular vectors. |
| S    | 4 * k          | float32 | Vector containing singular numbers          |
| Vt   | 4 * height * k | float32 | Matrix containing of right singular vector. |
