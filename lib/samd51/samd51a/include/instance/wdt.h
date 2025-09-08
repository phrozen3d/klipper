/***************************************************
函数名称：
输入参数：
返 回 值:
功能描述：蓝才刚-20231101
***************************************************/

#ifndef _SAMD51_WDT_INSTANCE_
#define _SAMD51_WDT_INSTANCE_

/* ========== Register definition for WDT peripheral ========== */
#if (defined(__ASSEMBLY__) || defined(__IAR_SYSTEMS_ASM__))
#define REG_WDT_CTRLA              (0x40002000) /**< \brief (WDT) Control */
#define REG_WDT_CONFIG             (0x40002001) /**< \brief (WDT) Configuration */
#define REG_WDT_EWCTRL             (0x40002002) /**< \brief (WDT) Early Warning Interrupt Control */
#define REG_WDT_INTENCLR           (0x40002004) /**< \brief (WDT) Interrupt Enable Clear */
#define REG_WDT_INTENSET           (0x40002005) /**< \brief (WDT) Interrupt Enable Set */
#define REG_WDT_INTFLAG            (0x40002006) /**< \brief (WDT) Interrupt Flag Status and Clear */
#define REG_WDT_SYNCBUSY           (0x40002008) /**< \brief (WDT) Synchronization Busy */
#define REG_WDT_CLEAR              (0x4000200C) /**< \brief (WDT) Clear */
#else
#define REG_WDT_CTRLA              (*(RwReg8 *)0x40002000UL) /**< \brief (WDT) Control */
#define REG_WDT_CONFIG             (*(RwReg8 *)0x40002001UL) /**< \brief (WDT) Configuration */
#define REG_WDT_EWCTRL             (*(RwReg8 *)0x40002002UL) /**< \brief (WDT) Early Warning Interrupt Control */
#define REG_WDT_INTENCLR           (*(RwReg8 *)0x40002004UL) /**< \brief (WDT) Interrupt Enable Clear */
#define REG_WDT_INTENSET           (*(RwReg8 *)0x40002005UL) /**< \brief (WDT) Interrupt Enable Set */
#define REG_WDT_INTFLAG            (*(RwReg8 *)0x40002006UL) /**< \brief (WDT) Interrupt Flag Status and Clear */
#define REG_WDT_SYNCBUSY           (*(RoReg  *)0x40002008UL) /**< \brief (WDT) Synchronization Busy */
#define REG_WDT_CLEAR              (*(WoReg8 *)0x4000200CUL) /**< \brief (WDT) Clear */
#endif /* (defined(__ASSEMBLY__) || defined(__IAR_SYSTEMS_ASM__)) */


#endif /* _SAMD51_WDT_INSTANCE_ */
