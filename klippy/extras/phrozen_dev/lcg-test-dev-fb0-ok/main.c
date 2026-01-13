/***************************************************************
项目名称：
芯片类型: 
功能: 
研发人员：蓝才刚-20240611
开发时间: 
**************************************************************/

#include <stdio.h>
#include <unistd.h>
#include <linux/fb.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/ioctl.h>





//typedef unsigned short color_t; //RGB565=16BIT
typedef unsigned int color_t; //RGB565=16BIT;RGB666=18BIT;RGB888=24BIT;



static struct fb_var_screeninfo __g_vinfo; /* 显示信息 */
static color_t *__gp_frame; /* 虚拟屏幕首地址 */





/***************************************************
函数名称：
输入参数：
返 回 值:
功能描述：蓝才刚-20250226
***************************************************/
void full_screen(color_t color) {
	int i;
	color_t *p = __gp_frame;

	for (i = 0; i < __g_vinfo.xres_virtual * __g_vinfo.yres_virtual; i++) {
		*p++ = color;
	}
}
/***************************************************
函数名称：
输入参数：
返 回 值:
功能描述：蓝才刚-20250226
***************************************************/
int framebuffer_init(void) {
	int fd = 0;
	fd = open("/dev/fb0", O_RDWR);
	printf("fd = %d\n", fd);
	
	if (fd == -1) {
		perror("fail to open /dev/fb0\n");
		return -1;
	}

	ioctl(fd, FBIOGET_VSCREENINFO, &__g_vinfo); /* 获取显示信息 */
	printf("bits_per_pixel = %d\n", __g_vinfo.bits_per_pixel); //一个像素点对应的位数，RGB565=16;RGB666=18;RGB888=24;
	printf("xres_virtual = %d\n", __g_vinfo.xres_virtual); /* 虚拟x轴像素点数 */
	printf("yres_virtual = %d\n", __g_vinfo.yres_virtual); /* 虚拟y轴像素点数 */
	printf("xres = %d\n", __g_vinfo.xres); /* x轴像素点数 */
	printf("yres = %d\n", __g_vinfo.yres); /* y轴像素点数 */

	__gp_frame = mmap(NULL, /* 映射区的开始地址，为NULL表示由系统决定映射区的起始地址 */
			__g_vinfo.xres_virtual * __g_vinfo.yres_virtual * __g_vinfo.bits_per_pixel / 8, /* 映射区大小 */
			PROT_WRITE | PROT_READ, /* 内存保护标志（可读可写） */
			MAP_SHARED, /* 映射对象类型（与其他进程共享） */
			fd, /* 有效的文件描述符 */
			0); /* 被映射内容的偏移量 */
			
	if (__gp_frame == NULL) {
		perror("fail to mmap\n");
		return -1;
	}
	
	return 0;
}


/***************************************************
函数名称：
输入参数：
返 回 值:
功能描述：蓝才刚-20250226
***************************************************/
int main() {
	if (framebuffer_init()) {
		return -1;
	}

	while (1) {
			// full_screen(0x001F);//RGB565;16BIT;0000 0000 0001 1111;蓝色
			// sleep(2);
			// full_screen(0x07E0);//0000 0111 1110 0000;绿色
			// sleep(2);
			// full_screen(0xF800);//1111 1000 0000 0000;红色
			// sleep(2);
			
			// full_screen(0x0000003F);//RGB666;18BIT;0000 0000 0000 0000 0000 0000 0011 1111;蓝色
			// sleep(2);
			// full_screen(0x00000FC0);//0000 0000 0000 0000 0000 1111 1100 0000;绿色
			// sleep(2);
			// full_screen(0x0003F000);//0000 0000 0000 0011 1111 0000 0000 0000;红色
			// sleep(2);
			
			
			full_screen(0x0000FF00);//0000 0000 0000 0000 1111 1111 0000 0000;绿色
			sleep(2);
			full_screen(0x00FF0000);//0000 0000 1111 1111 0000 0000 0000 0000;红色
			sleep(2);
			full_screen(0x000000FF);//RGB888;24BIT;0000 0000 0000 0000 0000 0000 1111 1111;蓝色
			sleep(2);
	}
	return 0;
}



