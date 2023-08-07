#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
// using namespace cv;

#include <string>
#include <iostream>
using namespace cv;
using namespace std;

int main() {
	cv::Mat img = cv::imread("./target.png");
	cv::Mat resize_img(img);
	resize(img, resize_img, cv::Size(img.cols / 7, img.rows / 7));
	cv::imshow("4K", resize_img);
	cv::waitKey(0);
	return 0;
}
