/*********************** dSPACE target specific file *************************

   Header file turbine_trc_ptr.h:

   Declaration of function that initializes the global TRC pointers

   RTI1401 7.11 (02-Nov-2018)
   Tue Jan 13 14:09:22 2026

   Copyright 2026, dSPACE GmbH. All rights reserved.

 *****************************************************************************/
#ifndef RTI_HEADER_turbine_trc_ptr_h_
#define RTI_HEADER_turbine_trc_ptr_h_

/* Include the model header file. */
#include "turbine.h"
#include "turbine_private.h"
#ifdef EXTERN_C
#undef EXTERN_C
#endif

#ifdef __cplusplus
#define EXTERN_C                       extern "C"
#else
#define EXTERN_C                       extern
#endif

/*
 *  Declare the global TRC pointers
 */
EXTERN_C volatile real_T *p_0_turbine_real_T_0;
EXTERN_C volatile real_T *p_1_turbine_real_T_0;

/*
 *  Declare the general function for TRC pointer initialization
 */
EXTERN_C void turbine_rti_init_trc_pointers(void);

#endif                                 /* RTI_HEADER_turbine_trc_ptr_h_ */
