using System;
using System.Drawing;
using System.IO;

namespace imagefilter
{
	class MainClass
	{
		public static void Main (string[] args)
		{
			Bitmap image1 = (Bitmap) Image.FromFile(args [0], true);


			if (args[1] == "red") {
				for (int x = 1; x <= image1.Width -1; x++)
				{
					for (int y = 1; y <= image1.Height - 1; y++)
					{
						Color mycolor = Color.FromArgb(image1.GetPixel (x, y).R, 0, 0);
						image1.SetPixel (x, y, mycolor);
					}
				}
				image1.Save (args[2], System.Drawing.Imaging.ImageFormat.Jpeg);
			} else if (args[1] == "greyscale") {
				for (int x = 1; x <= image1.Width -1; x++)
				{
					for (int y = 1; y <= image1.Height - 1; y++)
					{
						int br = Convert.ToInt32(image1.GetPixel (x, y).GetBrightness () * 255);
						Color mycolor = Color.FromArgb (br, br, br);
						image1.SetPixel (x, y, mycolor);
					}
				}
				image1.Save (args[2], System.Drawing.Imaging.ImageFormat.Jpeg);
			} else if (args[1] == "sepia") {
				for (int x = 1; x <= image1.Width -1; x++)
				{
					for (int y = 1; y <= image1.Height - 1; y++)
					{
						int r = Convert.ToInt32(image1.GetPixel (x, y).R * 0.393) + Convert.ToInt32(image1.GetPixel (x, y).G * 0.769) + Convert.ToInt32(image1.GetPixel (x, y).B * 0.189);
						int g = Convert.ToInt32(image1.GetPixel (x, y).R * 0.349) + Convert.ToInt32(image1.GetPixel (x, y).G * 0.686) + Convert.ToInt32(image1.GetPixel (x, y).B * 0.168);
						int b = Convert.ToInt32(image1.GetPixel (x, y).R * 0.272) + Convert.ToInt32(image1.GetPixel (x, y).G * 0.534) + Convert.ToInt32(image1.GetPixel (x, y).B * 0.131);
						if (r > 255) {r = 255;} ;
						if (g > 255) {g = 255;} ;
						if (b > 255) {b = 255;} ;

						Color mycolor = Color.FromArgb (r, g, b);
						image1.SetPixel (x, y, mycolor);
					}
				}
				image1.Save (args[2], System.Drawing.Imaging.ImageFormat.Jpeg);
			} else if (args[1] == "boxblur") {
				Bitmap origImage = image1;

				for (int x = 1; x <= origImage.Width -1; x++) {
					for (int y = 1; y <= origImage.Height - 1; y++) {

						double rsum = 0;
						double gsum = 0;
						double bsum = 0;

						int ni = 0;
						int nj = 0;

						for (int i = -1; i <= 1; i++) {
							for (int j = -1; j <= 1; j++) {
								if (x + i > origImage.Width - 1 | x + i < 0) {
									ni = i * -1;
								}
								if (y + j > origImage.Height - 1 | y + j < 0) {
									nj = j * -1;
								}

								rsum += origImage.GetPixel (x + i + ni, y + j + nj).R;
								gsum += origImage.GetPixel (x + i + ni, y + j + nj).G; 
								bsum += origImage.GetPixel (x + i + ni, y + j + nj).B;
							}
						}

						int rsumi = (int)(rsum / 9);
						int gsumi = (int)(gsum / 9); 
						int bsumi = (int)(bsum / 9);

						Color mycolor = Color.FromArgb (rsumi, gsumi, bsumi);
						image1.SetPixel (x, y, mycolor);
					}
				}
				image1.Save (args[2], System.Drawing.Imaging.ImageFormat.Jpeg);

			}
		}
	}
}
