/***************************************************
函数名称：
输入参数：
返 回 值:
功能描述：蓝才刚-20231101
***************************************************/

#ifndef _SAMD51_RSTC_INSTANCE_
#define _SAMD51_RSTC_INSTANCE_

/* ========== Register definition for RSTC peripheral ========== */
#if (defined(__ASSEMBLY__) || defined(__IAR_SYSTEMS_ASM__))
#define REG_RSTC_RCAUSE            (0x40000C00) /**< \brief (RSTC) Reset Cause */
#define REG_RSTC_BKUPEXIT          (0x40000C02) /**< \brief (RSTC) Backup Exit Source */
#else
#define REG_RSTC_RCAUSE            (*(RoReg8 *)0x40000C00UL) /**< \brief (RSTC) Reset Cause */
#define REG_RSTC_BKUPEXIT          (*(RoReg8 *)0x40000C02UL) /**< \brief (RSTC) Backup Exit Source */
#endif /* (defined(__ASSEMBLY__) || defined(__IAR_SYSTEMS_ASM__)) */

/* ========== Instance parameters for RSTC peripheral ========== */
#define RSTC_BACKUP_IMPLEMENTED     1       
#define RSTC_HIB_IMPLEMENTED        1       
#define RSTC_NUMBER_OF_EXTWAKE      0        // number of external wakeup line
#define RSTC_NVMRST_IMPLEMENTED     1       

#endif /* _SAMD51_RSTC_INSTANCE_ */
