;This code is modified from a1.pro
; HISORY : created on 7/25/2004 by L. Wang in the original codes based on Wang et al. (2003)
;	  largely modified and reorganized by J. Gong in 2007ish to process all HRRD data
;	  updated on 3/25/21 to adjust the reader to fit eclipse2020 format
;	  updated on 3/1/24 to remove some redundant functions and add comments for input data format requirement
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro check,Test_variable,ttl=ttl

;+
; NAME:
;  check
; PURPOSE:
;  does a help of the variable, and if it is an array
;  prints out the max and min
; CATEGORY:
;  debug
; CALLING SEQUENCE:
;   check,test_variable
; INPUTS:
;   test_variable = the variable to be inspected
; OPTIONAL INPUT PARAMETERS:
; KEYWORD PARAMETERS:
; OUTPUTS:
; OPTIONAL OUTPUT PARAMETERS:
; COMMON BLOCKS:
; SIDE EFFECTS:
; RESTRICTIONS:
; PROCEDURE:
; REQUIRED ROUTINES:
; MODIFICATION HISTORY:
;   mr schoeberl '88
;  idlv2 (lrlait) 900615
;-

on_error,2

cc=!c

v=size(Test_variable)
if v(0) eq 0 then begin
   help,Test_variable
endif else begin
   if not keyword_set(ttl) then begin
       help,Test_variable
       print,' Min =',min(Test_variable),' Max = ',max(Test_variable)
   endif else begin
       print,ttl+' Min =',min(Test_variable),' Max = ',max(Test_variable)
   endelse
endelse

!c=cc

return
end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
;purpose:       cal. k (zonal wavenumber)
;                    l (meridional wavenumber)
;               from
;                    phi (horizontal phase propagation direction)
;                    l_h (horizontal wavelength)
;
;input:
;
;output:
;
;algorithm:
;
;history:       09/16/04 created
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro phi2kl $

          ;input
          ,phi $        ;horizontal phase prop. dir., from East         [deg]
          ,l_h $        ;horizontal wavelength                          [km]

          ;output
          ,k $          ;zonal wavenumber                               [SI]
          ,l            ;meridional wavenumber                          [SI]

;kl=2.*!pi*1.e-3/l_h
;phi2=phi/180.*!pi
kl=2.e-3*!pi/l_h
phi2=phi*!dtor
k=kl*cos(phi2)
l=kl*sin(phi2)

return
end

;***********************************************************
FUNCTION Avg1D, A0, NoData=NoData, MinPts=MinPts
;+
; PURPOSE:
;       Returns average of 1-d array of data.
;
; CALLING SEQUENCE:
;       Avg1D, A, NoData=NoData, MinPts=MinPts
;
; INPUTS:
;       A:              input vector
;       NoData:         missing data value
;       MinPts:         minimum number of valid data in A (default: 1)
;
; OUTPUTS:
;       Returns TOTAL(WHERE(A NE NoData))/N_ELEMENTS(WHERE(A NE NoData))
;       if N_ELEMENTS(...) is greater then MinPts; returns NoData otherwise.
;_
a=reform(a0)
 IF KEYWORD_SET(MinPts) THEN _MinPts=MinPts ELSE _MinPts=1
 IF KEYWORD_SET(NoData) THEN BEGIN
   in = WHERE(A NE NoData, NIn)
   IF (NIn GE _MinPts) THEN Value=TOTAL(A(in))/NIn ELSE Value=NoData
 ENDIF ELSE Value=TOTAL(A)/N_ELEMENTS(A)
RETURN, Value
END; {Avg1D}

;-------------------------------------------------------------
;+
; NAME:
;       DATATYPE
; PURPOSE:
;       Datatype of variable as a string (3 char or spelled out).
; CATEGORY:
; CALLING SEQUENCE:
;       typ = datatype(var, [flag])
; INPUTS:
;       var = variable to examine.         in
;       flag = output format flag (def=0). in
; KEYWORD PARAMETERS:
;       Keywords:
;         /DESCRIPTOR returns a descriptor for the given variable.
;           If the variable is a scalar the value is returned as
;           a string.  If it is an array a description is return
;           just like the HELP command gives.  Ex:
;           datatype(fltarr(2,3,5),/desc) gives
;             FLTARR(2,3,5)  (flag always defaults to 3 for /DESC).
; OUTPUTS:
;       typ = datatype string or number.   out
;          flag=0    flag=1      flag=2    flag=3
;          UND       Undefined   0         UND
;          BYT       Byte        1         BYT
;          INT       Integer     2         INT
;          LON       Long        3         LON
;          FLO       Float       4         FLT
;          DOU       Double      5         DBL
;          COM       Complex     6         COMPLEX
;          STR       String      7         STR
;          STC       Structure   8         STC
;          DCO       DComplex    9         DCOMPLEX
; COMMON BLOCKS:
; NOTES:
; MODIFICATION HISTORY:
;       Written by R. Sterner, 24 Oct, 1985.
;       RES 29 June, 1988 --- added spelled out TYPE.
;       R. Sterner, 13 Dec 1990 --- Added strings and structures.
;       R. Sterner, 19 Jun, 1991 --- Added format 3.
;       R. Sterner, 18 Mar, 1993 --- Added /DESCRIPTOR.
;       R. Sterner, 1995 Jul 24 --- Added DCOMPLEX for data type 9.
;       Johns Hopkins University Applied Physics Laboratory.
;
; Copyright (C) 1985, Johns Hopkins University/Applied Physics Laboratory
; This software may be used, copied, or redistributed as long as it is not
; sold and this copyright notice is reproduced on each copy made.  This
; routine is provided as is without any express or implied warranties
; whatsoever.  Other limitations apply as described in the file disclaimer.txt.
;-
;-------------------------------------------------------------

	function datatype,var, flag0, descriptor=desc, help=hlp

	if (n_params(0) lt 1) or keyword_set(hlp) then begin
	  print,' Datatype of variable as a string (3 char or spelled out).'
	  print,' typ = datatype(var, [flag])'
	  print,'   var = variable to examine.         in'
	  print,'   flag = output format flag (def=0). in'
	  print,'   typ = datatype string or number.   out'
	  print,'      flag=0    flag=1      flag=2    flag=3'
	  print,'      UND       Undefined   0         UND'
	  print,'      BYT       Byte        1         BYT'
	  print,'      INT       Integer     2         INT'
	  print,'      LON       Long        3         LON'
	  print,'      FLO       Float       4         FLT'
	  print,'      DOU       Double      5         DBL'
	  print,'      COM       Complex     6         COMPLEX'
	  print,'      STR       String      7         STR'
	  print,'      STC       Structure   8         STC'
	  print,'      DCO       DComplex    9         DCOMPLEX'
	  print,' Keywords:'
	  print,'   /DESCRIPTOR returns a descriptor for the given variable.'
 	  print,'     If the variable is a scalar the value is returned as'
 	  print,'     a string.  If it is an array a description is return'
 	  print,'     just like the HELP command gives.  Ex:'
 	  print,'     datatype(fltarr(2,3,5),/desc) gives'
 	  print,'       FLTARR(2,3,5)  (flag always defaults to 3 for /DESC).'
	  return, -1
	endif

	if n_params(0) lt 2 then flag0 = 0	; Default flag.
	flag = flag0				; Make a copy.

	if n_elements(var) eq 0 then begin
	  s = [0,0]
	endif else begin
	  s = size(var)
	endelse

	if keyword_set(desc) then flag = 3

	if flag eq 2 then typ = s(s(0)+1)

	if flag eq 0 then begin
	  case s(s(0)+1) of
   0:	    typ = 'UND'
   1:       typ = 'BYT'
   2:       typ = 'INT'
   4:       typ = 'FLO'
   3:       typ = 'LON'
   5:       typ = 'DOU'
   6:       typ = 'COM'
   7:       typ = 'STR'
   8:       typ = 'STC'
   9:       typ = 'DCO'
else:       print,'Error in datatype'
	  endcase
	endif else if flag eq 1 then begin
	  case s(s(0)+1) of
   0:	    typ = 'Undefined'
   1:       typ = 'Byte'
   2:       typ = 'Integer'
   4:       typ = 'Float'
   3:       typ = 'Long'
   5:       typ = 'Double'
   6:       typ = 'Complex'
   7:       typ = 'String'
   8:       typ = 'Structure'
   9:       typ = 'DComplex'
else:       print,'Error in datatype'
	  endcase
	endif else if flag eq 3 then begin
	  case s(s(0)+1) of
   0:	    typ = 'UND'
   1:       typ = 'BYT'
   2:       typ = 'INT'
   4:       typ = 'FLT'
   3:       typ = 'LON'
   5:       typ = 'DBL'
   6:       typ = 'COMPLEX'
   7:       typ = 'STR'
   8:       typ = 'STC'
   9:       typ = 'DCOMPLEX'
else:       print,'Error in datatype'
	  endcase
	endif

	if ~ keyword_set(desc) then begin
	  return, typ					; Return data type.
	endif else begin
	  if s(0) eq 0 then return,strtrim(var,2)	; Return scalar desc.
	  aa = typ+'ARR('
          for i = 1, s(0) do begin
            aa = aa + strtrim(s(i),2)
            if i lt s(0) then aa = aa + ','
            endfor
          aa = aa+')'
	  return, aa
	endelse

	END
;********************************
PRO arc_circ,r,theta_s,df
; Procedure to plot arc of circle with radius r,
; starting angle theta_s over and arc length df
   x = fltarr(100)
   y = x
   x = replicate(r,100)
   y = findgen(100)*df/100+theta_s
   oplot,x,y,/polar
   xo = [0.,x*cos(y)]
   yo = [0.,x*sin(y)]
   polyfill,xo,yo,color = 200
   return
END
;-------------------------------------------------------------
;+
; NAME:
;       INTERPX
; PURPOSE:
;       Interpolate data with possible gaps and missing (bad) values.
; CATEGORY:
; CALLING SEQUENCE:
;       yy = interp1(x,y,xx)
; INPUTS:
;       x,y = input points.            in
;         x is assumed monotonically increasing.
;       xx = desired x values.         in
;         xx need not be monotonically increasing.
; KEYWORD PARAMETERS:
;       Keywords:
;         BAD=b  Values GREATER THAN b are considered missing.
;         GAP=g  Gaps in x greater than or equal to this
;           are broken by setting the output curve points
;           in the gaps to a flag value of 32000 or BAD if given.
;         /FIXBAD  means interpolate across bad data between
;           closest good points on each side.  Otherwise the
;           bad points are flagged with the value specified
;           for BAD.
; OUTPUTS:
;       yy = interpolated y values.    out
; COMMON BLOCKS:
; NOTES:
;       Notes: Flagged values may be used to break a plotted
;          curve using MAX_VALUE in the PLOT or OPLOT command:
;          plot,x,y,max_value=999
;          SLOW for more than a few thousand points.
; MODIFICATION HISTORY:
;       R. Sterner, 12 Aug, 1993
;
; Copyright (C) 1993, Johns Hopkins University/Applied Physics Laboratory
; This software may be used, copied, or redistributed as long as it is not
; sold and this copyright notice is reproduced on each copy made.  This
; routine is provided as is without any express or implied warranties
; whatsoever.  Other limitations apply as described in the file disclaimer.txt.
;-
;-------------------------------------------------------------

	function interpx, x,y,xx, help=hlp, bad=bad, $
	  gap=gap, fixbad=xbad

	if (n_params(0) lt 3) or keyword_set(hlp) then begin
	  print,' Interpolate data with possible gaps and missing (bad) values.'
	  print,' yy = interp1(x,y,xx)'
	  print,'   x,y = input points.            in'
	  print,'     x is assumed monotonically increasing.'
	  print,'   xx = desired x values.         in'
	  print,'     xx need not be monotonically increasing.'
	  print,'   yy = interpolated y values.    out'
	  print,' Keywords:'
	  print,'   BAD=b  Values GREATER THAN b are considered missing.'
	  print,'   GAP=g  Gaps in x greater than or equal to this'
	  print,'     are broken by setting the output curve points'
	  print,'     in the gaps to a flag value of 32000 or BAD if given.'
	  print,'   /FIXBAD  means interpolate across bad data between'
	  print,'     closest good points on each side.  Otherwise the'
	  print,'     bad points are flagged with the value specified'
	  print,'     for BAD.'
	  print,' Notes: Flagged values may be used to break a plotted'
	  print,'    curve using MAX_VALUE in the PLOT or OPLOT command:'
	  print,'    plot,x,y,max_value=999'
	  print,'    SLOW for more than a few thousand points.'
	  return,-1
	endif

	;--------  Find any data gaps  ------------------------------
	;  Data gaps are where the X coordinate jumps by more than a
	;  specified amount.  Save the index of the point just before
	;  the gap in glo and the index of the point just above the
	;  gap in ghi (= next point).
	;------------------------------------------------------------
	cntg = 0				; Assume no gaps.
	if n_elements(gap) ne 0 then begin	; Gap value given.
	  glo = where(x(1:*)-x gt gap, cntg)	; Index of 1st pt below gap.
	  ghi = glo + 1				; Index of 1st pt above gap.
	endif

	;--------  Find any bad points  -----------------------------------
	;  It is assumed that bad points have been tagged with a flag value
	;  before calling this routine.  Any points with a value less than
	;  or equal to the flag value are assumed to be good.  The indices
	;  of the good points on either side are saved in lo and hi.
	;-----------------------------------------------------------------
	cntb = 0				; Assume no bad points.
	if n_elements(bad) ne 0 then begin	; Bad tag value given.
	  w = where(y le bad, cnt)		; Indices of good values.
	  if cnt gt 0 then begin		; Found some good points.
	    wb = where(w(1:*)-w gt 1, cntb)	; Look for index jumps > 1.
	  endif
	endif
	if cntb gt 0 then begin	; Found some bad point groups.
	  lo = w(wb)		; Index of ignore window bottom.
	  hi = w(wb+1)		; Index of ignore window top.
	endif

	;--------  Setup output y array and flag value  -------
	yy = make_array(n_elements(xx),type=datatype(y,2))
	flag = 32000.
	if n_elements(bad) ne 0 then flag = bad

	;-----  Handle bad points  -------------------------------
	;  Flag which points in the output arrays to ignore due to bad pts.
	;---------------------------------------------------------
	if ~ keyword_set(xbad) then begin
	  if cntb gt 0 then begin
	    for i = 0, n_elements(lo)-1 do begin  ; Loop thru bad point gaps.
	      w = where((xx gt x(lo(i))) and (xx lt x(hi(i))), cnt) ; In gap.
	      if cnt gt 0 then yy(w) = flag	  ; Flag those in bad pt gap.
	    endfor
	  endif
	endif

	;-----  Handle data gaps  ---------------------------------
	;  Flag which points in the output arrays to ignore due to data gaps.
	;----------------------------------------------------------
	if cntg gt 0 then begin
	  for i = 0, n_elements(glo)-1 do begin	; Loop thru gaps.
	    w = where((xx gt x(glo(i))) and (xx lt x(ghi(i))), cnt)
	    if cnt gt 0 then yy(w) = flag		; Flag those in gap.
	  endfor
	endif

	;-----  Linearly interpolate into x,y at xx to get yy --------
	;  Drop any bad points from input curve before interpolating.
	;  Then find input and output curve sizes.
	;  Finally interpolate needed points.
	;-------------------------------------------------------------
	cnt = 0
	if n_elements(bad) ne 0 then begin
	  w = where(y lt bad, cnt)			; Drop bad points
	endif
	if cnt eq 0 then w = lindgen(n_elements(x))	; before interpolation.
	x2 = x(w)
	y2 = y(w)

	lstxx = n_elements(xx) - 1		; Number of output points.
	lstx = n_elements(x2) - 1		; Number of good input points.

	for i = 0L, lstxx do begin		; Loop through output points.
	  if yy(i) eq flag then goto, skip	; Ignore flagged points.
	  j = (where(x2 ge xx(i)))(0)
	  case 1 of
j eq -1:    yy(i) = y2(lstx)			; After last input x.
j eq  0:    yy(i) = y2(0)			; Before first input x.
   else:    begin				; Must interpolate.
	      m = (y2(j) - y2(j-1))/(x2(j) - x2(j-1))	; Slope.
	      yy(i) = m*(xx(i) - x2(j-1)) + y2(j-1)	; y = m*x + b.
	    end
	  endcase
skip:
	endfor

	return, yy
	end
;+
; NAME:
;   MPFIT
;
; AUTHOR:
;   Craig B. Markwardt, NASA/GSFC Code 662, Greenbelt, MD 20770
;   craigm@lheamail.gsfc.nasa.gov
;   UPDATED VERSIONs can be found on my WEB PAGE:
;      http://astrog.physics.wisc.edu/~craigm/idl.html
;
; PURPOSE:
;   Perform Levenberg-Marquardt least-squares minimization (MINPACK-1)
;
; MAJOR TOPICS:
;   Curve and Surface Fitting
;
; CALLING SEQUENCE:
;   parms = MPFIT(MYFUNCT, start_parms, FUNCTARGS=fcnargs, NFEV=nfev,
;                 MAXITER=maxiter, ERRMSG=errmsg, NPRINT=nprint,
;                 FTOL=ftol, XTOL=xtol, GTOL=gtol,
;                 STATUS=status, ITERPROC=iterproc, ITERARGS=iterargs,
;                 COVAR=covar, PERROR=perror,
;                 PARINFO=parinfo)
;
; DESCRIPTION:
;
;  MPFIT uses the Levenberg-Marquardt technique to solve the
;  least-squares problem.  In its typical use, MPFIT will be used to
;  fit a user-supplied function (the "model") to user-supplied data
;  points (the "data") by adjusting a set of parameters.
;
;  For example, a researcher may think that a set of observed data
;  points is best modelled with a Gaussian curve.  A Gaussian curve is
;  parameterized by its mean, standard deviation and normalization.
;  MPFIT will, within certain constraints, find the set of parameters
;  which best fits the data.  The fit is "best" in the least-squares
;  sense; that is, the sum of the weighted squared differences between
;  the model and data is minimumized.
;
;  The Levenberg-Marquardt technique is a particular strategy for
;  iteratively searching for the best fit.  This particular
;  implementation is drawn from MINPACK-1 (see NETLIB), and seems to
;  be more robust than routines provided with IDL.  This version
;  allows upper and lower bounding constraints to be placed on each
;  parameter, or the parameter can be held fixed.
;
;  The IDL user-supplied function should return an array of weighted
;  deviations between model and data.  In a typical scientific problem
;  the residuals should be weighted so that each deviate has a
;  gaussian sigma of 1.0.  If X represents values of the independent
;  variable, Y represents a measurement for each value of X, and ERR
;  represents the error in the measurements, then the deviates could
;  be calculated as follows:
;
;    DEVIATES = (Y - F(X)) / ERR
;
;  where F is the analytical function representing the model.  The
;  convenience functions MPFITFUN and MPFITEXPR calculate the deviates
;  for you.  If ERR are the 1-sigma uncertainties in Y, then
;
;    TOTAL( DEVIATES^2 )
;
;  will be the total chi-squared value.  MPFIT will minimize the
;  chi-square value.  The values of X, Y and ERR are passed through
;  MPFIT to the user-supplied function via the FUNCTARGS keyword.
;
;  MPFIT does not perform more general optimization tasks.  It is
;  customized, based on MINPACK-1, to the least-squares minimization
;  problem.
;
;  In the search for the best-fit solution, MPFIT calculates
;  derivatives numerically via a finite difference approximation.  The
;  user-supplied function need not calculate the derivatives
;  explicitly.
;
; INPUTS:
;   MYFUNCT - a string variable containing the name of the function to
;             be minimized.  The function should return the weighted
;             deviations between the model and the data.  It should be
;             declared in the following way (or in some equivalent):
;
;             FUNCTION MYFUNCT, p, X=x, Y=y, ERR=err
;              ; Parameter values are passed in "p"
;              ; Calculation of deviations occurs here
;              model = F(x)
;              return, (y-model)/err
;             END
;
;             The keyword parameters X, Y, and ERR in the example
;             above are suggestive but not required.  Any parameters
;             can be passed to MYFUNCT by using the FUNCTARGS keyword
;             to MPFIT.  Use MPFITFUN and MPFITEXPR if you need ideas
;             on how to do that.
;
;             In general there are no restrictions on the number of
;             dimensions in X, Y or ERR.  However the deviates *must*
;             be returned in a one-dimensional array, and must have
;             the same type (float or double) as the input arrays.
;
;   START_PARAMS - An array of starting values for each of the
;                  parameters of the model.  The number of parameters
;                  should be fewer than the number of measurements.
;                  Also, the parameters should have the same data type
;                  as the measurements (double is preferred).
;
;                  This parameter is optional if the PARINFO keyword
;                  is used.  See below.  The PARINFO keyword provides
;                  a mechanism to fix or constrain individual
;                  parameters.  If both START_PARAMS and PARINFO are
;                  passed, then the starting *value* is taken from
;                  START_PARAMS, but the *constraints* are taken from
;                  PARINFO.
;
; INPUT KEYWORD PARAMETERS:
;
;   FUNCTARGS - A structure which contains the parameters to be passed
;               to the user-supplied function specified by MYFUNCT via
;               the _EXTRA mechanism.  This is the way you can pass
;               data to your user-supplied function without using
;               common blocks.
;
;               Consider the following example:
;                if FUNCTARGS = { XVAL:[1.D,2,3], YVAL:[1.D,4,9],
;                                 ERRVAL:[1.D,1,1] }
;                then the user supplied function should be declared
;                like this:
;                PRO MYFUNCT, P, XVAL=x, YVAL=y, ERRVAL=err
;
;               By default, no extra parameters are passed to the
;               user-supplied function.
;
;   MAXITER - The maximum number of iterations to perform.  If the
;             number is exceeded, then the STATUS value is set to 5
;             and MPFIT returns.
;             Default: 200 iterations
;
;   FTOL - a nonnegative input variable. Termination occurs when both
;          the actual and predicted relative reductions in the sum of
;          squares are at most FTOL.  Therefore, FTOL measures the
;          relative error desired in the sum of squares.
;          Default: 1D-10
;
;   XTOL - a nonnegative input variable. Termination occurs when the
;          relative error between two consecutive iterates is at most
;          XTOL. therefore, XTOL measures the relative error desired
;          in the approximate solution.
;          Default: 1D-10
;
;   GTOL - a nonnegative input variable. Termination occurs when the
;          cosine of the angle between fvec and any column of the
;          jacobian is at most GTOL in absolute value. Therefore, GTOL
;          measures the orthogonality desired between the function
;          vector and the columns of the jacobian.
;          Default: 1D-10
;
;   ITERPROC - The name of a procedure to be called upon each NPRINT
;              iteration of the MPFIT routine.  It should be declared
;              in the following way:
;
;              PRO ITERPROC, MYFUNCT, p, iter, FUNCTARGS=fcnargs, $
;                PARINFO=parinfo, QUIET=quiet, ...
;                ; perform custom iteration update
;              END
;
;              Where MYFUNCT is the user-supplied function to be
;              minimized, P is the current set of model parameters,
;              ITER is the iteration number, and FUNCTARGS are the
;              arguments to be passed to MYFUNCT.  QUIET is set when
;              no textual output should be printed.  See below for
;              documentation of PARINFO.
;
;              In implementation, ITERPROC, can perform updates to the
;              terminal or graphical user interface, to provide
;              feedback while the fit proceeds.  If the fit is to be
;              stopped for any reason, then ITERPROC should set the
;              system variable !ERR to a negative value.  In
;              principle, ITERPROC should probably not modify the
;              parameter values, because it may interfere with the
;              algorithm's stability.  In practice it is allowed.
;
;              Default: an internal routine is used to print the
;                       parameter values.
;
;   NPRINT - The frequency with which ITERPROC is called.  A value of
;            1 indicates that ITERPROC is called with every iteration,
;            while 2 indicates every other iteration, etc.
;            Default value: 1
;
;   ITERARGS - The keyword arguments to be passed to ITERPROC via the
;              _EXTRA mechanism.  This should be a structure, and is
;              similar in operation to FUNCTARGS.
;              Default: no arguments are passed.
;
;   PARINFO - Provides a mechanism for more sophisticated constraints
;             to be placed on parameter values.  When PARINFO is not
;             passed, then it is assumed that all parameters are free
;             and unconstrained.  No values in PARINFO are modified
;             during the call to MPFIT.
;
;             PARINFO should be an array of structures, one for each
;             parameter.  Each parameter is associated with one
;             element of the array, in numerical order.  The structure
;             should have at least the following entries:
;
;               - VALUE - the starting parameter value (but see
;                         START_PARAMS above).
;
;               - FIXED - a boolean value, whether the parameter is to
;                         be held fixed or not.  Fixed parameters are
;                         not varied by MPFIT, but are passed on to
;                         MYFUNCT for evaluation.
;
;               - LIMITED - a two-element boolean array.  If the
;                 first/second element is set, then the parameter is
;                 bounded on the lower/upper side.  A parameter can be
;                 bounded on both sides.
;
;               - LIMITS - a two-element float or double array.  Gives
;                 the parameter limits on the lower and upper sides,
;                 respectively.  Zero, one or two of these values can
;                 be set, depending on the value of LIMITED.
;
;               - STEP - the step size to be used in calculating the
;                 numerical derivatives.  If set to zero, then the
;                 step size is computed automatically.
;
;             Other tag values can also be given in the structure, but
;             they are ignored.
;
;             Example:
;             parinfo = replicate({value:0.D, fixed:0, $
;                           limited:[0,0], limits:[0.D,0], step:0.D}, 5)
;             parinfo(0).fixed = 1
;             parinfo(1).limited(4) = 1
;             parinfo(1).limits(4)  = 50.D
;             parinfo(*).value = [5.7D, 2.2, 500., 1.5, 2000.]
;
;             A total of 5 parameters, with starting values of 5.7,
;             2.2, 500, 1.5, and 2000 are given.  The first parameter
;             is fixed at a value of 5.7, and the last parameter is
;             constrained to be above 50.
;
;             Default value:  all parameters are free and unconstrained.
;
;   QUIET - set this keyword when no textual output should be printed
;           by MPFIT
;
;   NOCOVAR - set this keyword to prevent the calculation of the
;             covariance matrix before returning (see COVAR)
;
; RETURNS:
;
;   Returns the array of best-fit parameters.
;
; OUTPUT KEYWORD PARAMETERS:
;
;   NFEV - the number of MYFUNCT function evaluations performed.
;
;   ERRMSG - a string error or warning message is returned.
;
;   BESTNORM - the value of the summed squared residuals for the
;              returned parameter values.
;
;   PERROR - The formal 1-sigma errors in each parameter.  If a
;            parameter is held fixed, or if it touches a boundary,
;            then the error is reported as zero.
;
;   COVAR - the covariance matrix for the set of parameters returned
;           by MPFIT.  The matrix is NxN where N is the number of
;           parameters.  The square root of the diagonal elements
;           gives the formal 1-sigma statistical errors on the
;           parameters IF errors were treated "properly" in MYFUNC.
;           Parameter errors are also returned in PERROR.
;
;           To compute the correlation matrix, PCOR, use this:
;           IDL> PCOR = COV * 0
;           IDL> FOR i = 0, n-1 DO FOR j = 0, n-1 DO $
;                PCOR(i,j) = COV(i,j)/sqrt(COV(i,i)*COV(j,j))
;
;           If NOCOVAR is set or MPFIT terminated abnormally, then
;           COVAR is set to a scalar with value !VALUES.D_NAN.
;
;   STATUS - an integer status code is returned.  It can have one of
;            the following values:
;
;	   0  improper input parameters.
;
;	   1  both actual and predicted relative reductions
;	      in the sum of squares are at most FTOL.
;
;	   2  relative error between two consecutive iterates
;	      is at most XTOL
;
;	   3  conditions for STATUS = 1 and STATUS = 2 both hold.
;
;	   4  the cosine of the angle between fvec and any
;	      column of the jacobian is at most GTOL in
;	      absolute value.
;
;	   5  the maximum number of iterations has been reached
;
;	   6  FTOL is too small. no further reduction in
;	      the sum of squares is possible.
;
;	   7  XTOL is too small. no further improvement in
;	      the approximate solution x is possible.
;
;	   8  GTOL is too small. fvec is orthogonal to the
;	      columns of the jacobian to machine precision.
;
; EXAMPLE:
;
;   p0 = [5.7D, 2.2, 500., 1.5, 2000.]
;   fa = {X:x, Y:y, ERR:err}
;   p = mpfit('MYFUNCT', p0, functargs=fa)
;
;   Minimizes sum of squares of MYFUNCT.  MYFUNCT is called with the X,
;   Y, and ERR keyword parameters that are given by FUNCTARGS.  The
;   resulting parameter values are returned in p.
;
; REFERENCES:
;
;   MINPACK-1, Jorge More', available from netlib (www.netlib.org).
;   "Optimization Software Guide," Jorge More' and Stephen Wright,
;     SIAM, *Frontiers in Applied Mathematics*, Number 14.
;
; MODIFICATION HISTORY:
;   Translated from MINPACK-1 in FORTRAN, Apr-Jul 1998, CM
;   Fixed bug in parameter limits (x vs xnew), 04 Aug 1998, CM
;   Added PERROR keyword, 04 Aug 1998, CM
;
;-

FUNCTION Welch,n
;Procedure for calculating Welch Window function (Num Recipes, p 422)
j = findgen(n)
nn = (n-1.)/2.
nd = (n+1.)/2.
RETURN, 1. - ((j - nn)/nd)^2
END ; End Welch
PRO functc,x,a,f,pder
; Return a function value in f.
; based on lmfunct
; Function for fitting modified Desaubies spectrum
; 23 June 1998 RAV
; F = Ao mu/(1+mu^A2)
; where mu = x/A1

;
;a(0)=F_0
;a(1)=m_*
;a(2)=t+1
;
   mu = x/a(1)				;m/m*
   d = mu^a(2)				;(m/m*)^t
   b = 1./(1+d)
   c = mu*b
   f = a(0)*c				;f0 (m/m*) / (1+(m/m*)^(t+1))
   IF (n_params() GE 4) THEN $
    pder = [ [f/a(0)],  $
             [-f*b*(1+(1-a(2))*d)/a(1)],  $
             [-f*b*alog(mu)*d] ]
   return
END

;
;for one sounding
;
;*****************************************************
PRO stokes_new,u,v,u_m,v_m,theta,n_bar,f_w,df,z30,no_correct=no_correct

;Procedure to calculate Stokes parameters for vertical
;wavenumber spectra
;*****************************************************
;Fourier transform velocity profiles, assumed to be at
;30 m spacing
; theta is azimuth computed from <u'T90>
   a = size(u)
   n = a(1)
   na = n/2

   is = fltarr(na)
   ds = is & ps = is & qs = is & df = is & phi = is
   df = 0.
   xd = df & yd = df & phi = df & axr = df
      ut = fft(u, -1)
      vt = fft(v, -1)

;Form Stokes parameters following Eckermann and Vincent (1989)
      it = float(ut*conj(ut) + vt*conj(vt))
      dt = float(ut*conj(ut) - vt*conj(vt))
      pt = 2.0*float(conj(ut)*vt)
      qt = 2.0*imaginary(conj(ut)*vt)

      is = it(1:na) & ds = dt(1:na)
      ps = pt(1:na) & qs = qt(1:na)

      df  = sqrt(total(qt(0:na))^2 + total(pt(0:na))^2 +  $
                    total(dt(0:na))^2)/total(it(0:na))
      phi = atan(total(pt), total(dt))/2.

      xi = asin(abs(total(qt(0:na))/(df*total(it(0:na)))))/2.0
      axr = 1.0/tan(xi)
; Correct for tranverse shear term
   u_t = fltarr(a(1))
   du_t_dz = 0.
   u_t = u_m*cos(theta)-v_m*sin(theta)
;stop
   du_t_dz = total(deriv(z30,u_t))/float(a(1))
;  axr_corr = du_t_dz/n_bar
   axr_corr = du_t_dz/n_bar
   if keyword_set(no_correct) then f_w = axr $
   else f_w = axr-axr_corr
   return
END ; End Stokes

PRO phase_speed_new,u_m,v_m,phi,up,vp,f,n_bar,f_w,m_bar,k_bar, $
                omega,c_z,c_i,c_x,c_y,df,c_ix,c_iy,c_gx,c_gy, $
;               c_xcomp,c_ycomp
                c_xcomp,c_ycomp, u_mean, u_mm, v_mm, theta,dzm
;stop
; Procedure to compute phase speeds
   a = size(up)
;  b = where(f_w GT 1 AND f_w LE 10, n_good)
;compute azimuth of mean winda = size(up)
   u_mm = reform(rebin(u_m,1))
   v_mm = reform(rebin(v_m,1))
   theta = atan(u_mm,v_mm)
   u_mean = sqrt(u_mm^2+v_mm^2)
;  mean_spec,up,vp,m_bar,m,lz,1,30.
;stop
   mean_spec_new,up,vp,m_bar,m,lz,1,dzm

   m_z = 2.0*!pi*m_bar

; First compute horizontal wavenumber
   k_bar = 0.
   k_bar = f*m_z*sqrt(f_w^2-1)/n_bar
   l_x = 2.0*!pi/k_bar

; Find intrinsic phase speeds
   c_z = f*f_w/(m_z)
   c_i = f*f_w/k_bar
   c_ix = c_i*sin(phi)
   c_iy = c_i*cos(phi)

; Now compute group velocity c_g = c_i + U
   c_gx = c_ix + u_mm
   c_gy = c_iy + v_mm
;plot_cg,c_gx,c_gy

; Find ground based phase speed, c
; and ground-based frequency
   omega = f*f_w + k_bar*u_mean*cos(theta-phi)
   c =  abs((c_i + u_mean*cos(theta-phi)))
   c_x = c/sin(phi)      ; note division since not true component velocity
   c_y = c/cos(phi)
   c_xcomp = (c_i + u_mean*cos(theta-phi))*sin(phi)
   c_ycomp = (c_i + u_mean*cos(theta-phi))*cos(phi)

   return
END                             ; End of phase speed

;using a complete dispersion relation
PRO phase_speed_new2,u_m,v_m,phi,up,vp,f,n_bar,f_w,m_bar,k_bar, $
                omega,c_z,c_i,c_x,c_y,df,c_ix,c_iy,c_gx,c_gy, $
;               c_xcomp,c_ycomp
                c_xcomp,c_ycomp, u_mean, u_mm, v_mm, theta,dzm,alpha
;stop
; Procedure to compute phase speeds
   a = size(up)
;  b = where(f_w GT 1 AND f_w LE 10, n_good)
;compute azimuth of mean winda = size(up)
   u_mm = reform(rebin(u_m,1))
   v_mm = reform(rebin(v_m,1))
   theta = atan(u_mm,v_mm)
   u_mean = sqrt(u_mm^2+v_mm^2)
;  mean_spec,up,vp,m_bar,m,lz,1,30.
;stop
   mean_spec_new,up,vp,m_bar,m,lz,1,dzm

   m_z = 2.0*!pi*m_bar

; First compute horizontal wavenumber
;  k_bar = f*m_z*sqrt(f_w^2-1)/n_bar
;  if abs(f*f_w) ge n_bar then message,'frequency too high'
   k_bar = f*sqrt(m_z^2+alpha^2)*sqrt(f_w^2-1)/sqrt(n_bar^2-(f*f_w)^2)
   l_x = 2.0*!pi/k_bar
;print,sqrt(f_w^2-1)
;print,sqrt(n_bar^2-(f*f_w)^2)
;print,k_bar
;print,k_bar
;print,l_x/1000.

; Find intrinsic phase speeds
   c_z = f*f_w/(m_z)
   c_i = f*f_w/k_bar
   c_ix = c_i*sin(phi)
   c_iy = c_i*cos(phi)

; Now compute group velocity c_g = c_i + U
   c_gx = c_ix + u_mm
   c_gy = c_iy + v_mm
;plot_cg,c_gx,c_gy

; Find ground based phase speed, c
; and ground-based frequency
   omega = f*f_w + k_bar*u_mean*cos(theta-phi)
   c =  abs((c_i + u_mean*cos(theta-phi)))
   c_x = c/sin(phi)      ; note division since not true component velocity
   c_y = c/cos(phi)
   c_xcomp = (c_i + u_mean*cos(theta-phi))*sin(phi)
   c_ycomp = (c_i + u_mean*cos(theta-phi))*cos(phi)

   return
END                             ; End of phase speed

;************************************************************
PRO directions_new,up,vp,tp,rho,phi,ut,vt,uq,vq,ui,vi   ;newly modified

; Procedure to compute mean direction of wave propagation
; from velocity and normalized temperature perturbations.
; Use covariances <u'T'+90> and <v'T'+90> to determine
; azimuth from North. Where T'+90 is the value of
; temperature after shifting phase by +90 deg via Hilbert
; transform.

   a=size(up)
   phi = 0.                                     ;dir of wave propagation
   ut = phi & vt = phi
   uq = ut & ui = ut
   vq = ut                                              ;newly added
; Carry out Hilbert transform
      to = float(HILBERT(tp, -1))

      ti = tp
      x = total(to*up*rho)/float(a(1))  ;column average
      y = total(to*vp*rho)/float(a(1))  ;column average
      ut = x
      vt = y
      uq = total(to*up)/n_elements(to)
      vq = total(to*vp)/n_elements(to)          ;newly added
      ui = total(ti*up)/n_elements(ti)
; Phi is azimuth from north
      phi = atan(x, y)
   return
END                             ; End Directions

;*************************************************
PRO t_spec_new,t,tspec,err,m,lamda,navr,cpm
; Procedure to calulate vertical-wavenumber power spectrum for temperature
; m and lamda are the output vertical wavenumber and scale arrays
; averaged over navr points
; cpm is the sample spacing in metres
; tspec is the output array (real) of length npts/navr
; err is a standard deviation of the tspec at each wavenumber
; Generate window function
; Average over all available observations if necessary
   a=size(t)
   npts=a(1)
;  IF (a(0) EQ 2) THEN n_obs = a(2) $
;   ELSE n_obs = 1
   n_obs = 1
   window = welch(npts)
   nred = npts/navr
   ts = fltarr(npts)
   tsq =fltarr(npts)
   nmax=npts-1
   nf = float(npts)/(total(window*window))

   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   if (navr ne 1) then m = m + delm/2.		; ? my question
   m(0) = delm/2.
   uf = complex((t(0:nmax)-total(t(0:nmax))/npts)*window ,0.0)
   ut = fft(uf,-1)
   spec = float(ut*conj(ut))
   ts = ts +spec
   tsq =spec*spec+tsq
;stop,'777'

   fnp =float(n_obs)
   norm = float(2*navr)*nf/(n_obs*delm) ; NB One-sided spectrum
   err = tsq/fnp - ts*ts/(fnp*fnp)
   err = fnp*sqrt(err)
   tspec = rebin(ts,nred)*norm
   tspec = tspec(0:npts/2)
;  err = rebin(err,nred)*norm
   err = 0.1*abs(ts)*norm			;I add this
   err = err(0:npts/2)
   lamda = 1.0/(m*1000)

return
END ; t_spec_new

PRO mean_spec_new,u,v,m_bar,m,lamda,navr,cpm
;Procedure to calulate mean vertical-wavenumber for wind components
;m and lamda are the output vertical wavenumber and wavelength arrays
;averaged over navr points
;cpm is the sample spacing in metres
;uspec and vspec are the output arrays (real) of length npts/navr
;Generate window function
;m_bar is the number of mean wavenumbers
   a=size(u)
   npts=a(1)
   n2 = npts/2
;  IF (a(0) EQ 2) THEN n_data = a(2)
;  m_bar = reform(fltarr(n_data))
   m_bar = 0.
   window = welch(npts)
   nred = npts/navr
   nmax=npts-1
   nf = float(npts)/(total(window*window))

   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   IF (navr NE 1) THEN  m = m + delm/2.
   m(0) = delm/2.
   norm = float(navr)*nf/delm

   i = complex(0,1)
;  IF (n_data GT 1) THEN BEGIN
;     FOR i = 0, n_data-1 DO BEGIN
         uf = (u(0:nmax)-total(u(0:nmax))/npts)*window
         vf = (v(0:nmax)-total(v(0:nmax))/npts)*window
         ut = fft(uf, -1)
         us = float(ut*conj(ut))
         vt = fft(vf, -1)
         vs = float(vt*conj(vt))
         us =  us + vs

         if (navr ne 1) THEN  $
          us = rebin(us, nred)*norm  $
         ELSE  $
          us = us*norm

         m_bar = rebin(us(1:n2)*m(1:n2),1)/rebin(us(1:n2),1)
;     ENDFOR
;  ENDIF
   lamda  = 1.0/(m*1000.0)
   RETURN
END

PRO directions_new_bandpass,up,vp,tp,rho,phi
; Procedure to compute mean direction of wave propagation
; from velocity and normalized temperature perturbations.
; Use covariances <u'T'+90> and <v'T'+90> to determine
; azimuth from North. Where T'+90 is the value of
; temperature after shifting phase by +90 deg via Hilbert
; transform.

   a=size(up)
   phi = 0.					;dir of wave propagation
   ut = phi & vt = phi
   uq = ut & ui = ut
   vq = ut						;newly added
; Carry out Hilbert transform
      to = float(HILBERT(tp, -1))

      ti = tp
      x = total(to*up*rho)/float(a(1))	;column average
      y = total(to*vp*rho)/float(a(1))	;column average
; Phi is azimuth from north
      phi = atan(x, y)
   return
END                             ; End Directions

pro get_perturbation,up,vp,tp,tb,um,vm,npoly
s=size(up)

zkm=findgen(s(1))*0.03

;--> uraw,vraw,traw
for i=0,s(2)-1 do begin
    if up(0,i) ne -999. and up(0,i) ne 999. then begin
        uraw=reform(up(*,i)+um(*,i))
        vraw=reform(vp(*,i)+vm(*,i))
        co = poly_fit(double(zkm),double(uraw),npoly,fitu)
        co = poly_fit(double(zkm),double(vraw),npoly,fitv)
        um(*,i)=fitu
        vm(*,i)=fitv
        up(*,i)=uraw-fitu
        vp(*,i)=vraw-fitv
    endif
    if tp(0,i) ne -999. and tp(0,i) ne 999. then begin
        traw=reform(tp(*,i)+tb(*,i))
        co = poly_fit(double(zkm),double(traw),npoly,fitt)
        tb(*,i)=fitt
        tp(*,i)=traw-fitt
    endif
endfor

return
end

pro get_perturbation_ltm,up,vp,tp,tb,um,vm,mn,ultm,vltm,tltm,npoly
s=size(up)

zkm=findgen(s(1))*0.03

;--> uraw,vraw,traw
for i=0,s(2)-1 do begin
    j=mn(i)-1
    if up(0,i) ne -999. and up(0,i) ne 999. then begin
        if ultm(0,j) eq -999. then stop
        if vltm(0,j) eq -999. then stop
        uraw=reform(up(*,i)+um(*,i))-ultm(*,j)
        vraw=reform(vp(*,i)+vm(*,i))-vltm(*,j)
        co = poly_fit(double(zkm),double(uraw),npoly,fitu)
        co = poly_fit(double(zkm),double(vraw),npoly,fitv)
        um(*,i)=fitu+ultm(*,j)
        vm(*,i)=fitv+vltm(*,j)
        up(*,i)=uraw-fitu
        vp(*,i)=vraw-fitv
    endif
    if tp(0,i) ne -999. and tp(0,i) ne 999. then begin
        if tltm(0,j) eq -999. then stop
        traw=reform(tp(*,i)+tb(*,i))-tltm(*,j)
        co = poly_fit(double(zkm),double(traw),npoly,fitt)
        tb(*,i)=fitt+tltm(*,j)
        tp(*,i)=traw-fitt
    endif
endfor

return
end
;**************************************************
pro get_high_pass,up,vp,tp,tb,um,vm,bndy
s=size(up)

zkm=findgen(s(1))*0.03

fhigh=1
flow=2*0.03/bndy

;--> uraw,vraw,traw
for i=0,s(2)-1 do begin
    if up(0,i) ne -999. and up(0,i) ne 999. then begin
        uraw=reform(up(*,i)+um(*,i))
        vraw=reform(vp(*,i)+vm(*,i))
        co = poly_fit(double(zkm),double(uraw),1,fitu)
        co = poly_fit(double(zkm),double(vraw),1,fitv)
        uraw=uraw-fitu
        vraw=vraw-fitv
        um(*,i)=digital_smooth(uraw,flow,fhigh)+fitu
        vm(*,i)=digital_smooth(vraw,flow,fhigh)+fitv
        up(*,i)=uraw-um(*,i)+fitu
        vp(*,i)=vraw-vm(*,i)+fitv
    endif
    if tp(0,i) ne -999. and tp(0,i) ne 999. then begin
        traw=reform(tp(*,i)+tb(*,i))
        co = poly_fit(double(zkm),double(traw),1,fitt)
        traw=traw-fitt
        tb(*,i)=digital_smooth(traw,flow,fhigh)+fitt
        tp(*,i)=traw-tb(*,i)+fitt
    endif
endfor

return
end

;*********************************************
PRO fit6, ts,sigma,m,a
; exactly the same as fit, but with t already being estimated previously
; and only fit ms and f0

   dummystring = ' '
   npt = n_elements(m)          ; Make spectrum one-sided
   n = npt/2.-1
   s = ts(1:n)
   x = m(1:n)
   ss = sigma(1:n)
; Make initial guess of fitting constants
; Get mean-square normalized temperature
   dm = m(4)-m(3)
   ts_bar = total(s)*dm
; Next mean wavenumber
   m_bar = total(s*x)*dm/ts_bar
; First guess at m_star
   ms = x(1)
   fo = ts_bar/ms

;  t = 4.0
;  a = [fo,ms,t ]
   a = [fo,ms]

   fa = {X:x, Y:s, ERR:ss}

   functc2,x,a,f        ; f is starting model

   deviates = (s-f)
; fitting a model to the avaerage spectrum using fitting algorithm
; embodied in mpfit.pro

   p_fit = mpfit('mp_funct2',a,functargs= fa,/QUIET)

   functc2,x,p_fit,spec_fit      ; evaluate fitted function

   a = p_fit
   return
END
;*********************************************
PRO mean_spec2,u,v,m_bar,m,lamda,navr,cpm
;
; exactly the same as mean_spec but calling welch2 instead of welch
;
;Procedure to calulate mean vertical-wavenumber for wind components
;m and lamda are the output vertical wavenumber and wavelength arrays
;averaged over navr points
;cpm is the sample spacing in metres
;uspec and vspec are the output arrays (real) of length npts/navr
;Generate window function
;m_bar is the number of mean wavenumbers
   a=size(u)
   npts=a(1)
   n2 = npts/2
   IF (a(0) EQ 2) THEN n_data = a(2)
   m_bar = reform(fltarr(n_data))
   window = welch2(npts)
   nred = npts/navr
   nmax=npts-1
   nf = float(npts)/(total(window*window))

   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   IF (navr NE 1) THEN  m = m + delm/2.
   m(0) = delm/2.
   norm = float(navr)*nf/delm

   i = complex(0,1)
   IF (n_data GT 1) THEN BEGIN
      FOR i = 0, n_data-1 DO BEGIN
         uf = (u(0:nmax,i)-total(u(0:nmax,i))/npts)*window
         vf = (v(0:nmax,i)-total(v(0:nmax,i))/npts)*window
         ut = fft(uf, -1)
         us = float(ut*conj(ut))
         vt = fft(vf, -1)
         vs = float(vt*conj(vt))
         us =  us + vs

         if (navr ne 1) THEN  $
          us = rebin(us, nred)*norm  $
         ELSE  $
          us = us*norm

         m_bar(i) = rebin(us(1:n2)*m(1:n2),1)/rebin(us(1:n2),1)
      ENDFOR
   ENDIF
   lamda  = 1.0/(m*1000.0)
   RETURN
END

PRO t_spec2,t,tspec,err,m,lamda,navr,cpm
;
; exactly the same as t_spec but calling welch2 instead of welch
;
; Procedure to calulate vertical-wavenumber power spectrum for temperature
; m and lamda are the output vertical wavenumber and scale arrays
; averaged over navr points
; cpm is the sample spacing in metres
; tspec is the output array (real) of length npts/navr
; err is a standard deviation of the tspec at each wavenumber
; Generate window function
; Average over all available observations if necessary
   a=size(t)
   npts=a(1)
   IF (a(0) EQ 2) THEN n_obs = a(2) $
    ELSE n_obs = 1
   window = welch2(npts)
   nred = npts/navr
   ts = fltarr(npts)
   tsq =fltarr(npts)
   nmax=npts-1
   nf = float(npts)/(total(window*window))

   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   if (navr ne 1) then m = m + delm/2.		; ? my question
   m(0) = delm/2.
   FOR i = 0,n_obs-1 DO BEGIN
      uf = complex((t(0:nmax,i)-total(t(0:nmax,i))/npts)*window ,0.0)
      ut = fft(uf,-1)
      spec = float(ut*conj(ut))
      ts = ts +spec
      tsq =spec*spec+tsq
   ENDFOR
   fnp =float(n_obs)
   norm = float(2*navr)*nf/(n_obs*delm) ; NB One-sided spectrum
   err = tsq/fnp - ts*ts/(fnp*fnp)
   err = fnp*sqrt(err)
   tspec = rebin(ts,nred)*norm
   tspec = tspec(0:npts/2)
   err = rebin(err,nred)*norm
   err = err(0:npts/2)
   lamda = 1.0/(m*1000)
return
END ; t_spec

PRO rotary_spec2,u,v,acp,ccp,m,lamda,navr,cpm
;
; exactly the same as rotary_spec but call welch2 instead of welch
;
;Procedure to calulate vertical-wavenumber power spectrum for wind components
;m and lamda are the output vertical wavenumber and wavelength arrays
;averaged over navr points
;cpm is the sample spacing in metres
;uspec and vspec are the output arrays (real) of length npts/navr

;Generate window function
   a=size(u)
   npts=a(1)
   n2 = npts/2
   IF (a(0) EQ 2) THEN n_data = a(2) ELSE n_DATA =1
   window = welch2(npts)
   nred = npts/navr
   nmax=npts-1
   nf = float(npts)/(total(window*window))
   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   IF (navr NE 1) THEN m = m + delm/2.
   m(0) = delm/2.
   norm = float(navr)*nf/delm
   acp = fltarr(n2) & ccp = acp

   FOR i = 0,n_data-1 DO BEGIN
      uf = (u(0:nmax,i)-total(u(0:nmax,i))/npts)*window
      vf = (v(0:nmax,i)-total(v(0:nmax,i))/npts)*window
      ut = fft(complex(uf,vf), -1)
      us = float(ut*conj(ut))
      IF (navr NE 1) THEN  $
       us = rebin(us,nred)*norm ELSE us = us*norm
;Anticlockwise component is positive half space
;clockwise component is negative half space
      acp = us(1:n2)+acp
      ccp = rotate(us(n2:nmax),2)+ccp
   ENDFOR
   acp = acp/float(n_data)
   ccp = ccp/float(n_data)
   lamda  = 1.0/(m*1000.0)
   return
END                             ; End rotary_spec
PRO phase_speed2,u_m,v_m,phi,up,vp,f,n_bar,f_w,m_bar,k_bar, $
                omega,c_z,c_i,c_x,c_y,df,c_ix,c_iy,c_gx,c_gy, $
;               c_xcomp,c_ycomp
                c_xcomp,c_ycomp, u_mean, u_mm, v_mm, theta
;
; exactly the same as phase_speed but call mean_spec2 instead of mean_spec
;
; Procedure to compute phase speeds
   a = size(up)
   b = where(f_w GT 1 AND f_w LE 10, n_good)
;compute azimuth of mean winda = size(up)
   u_mm = reform(rebin(u_m,1,a(2)))
   v_mm = reform(rebin(v_m,1,a(2)))
   theta = atan(u_mm,v_mm)
   u_mean = sqrt(u_mm^2+v_mm^2)
   mean_spec2,up,vp,m_bar,m,lz,1,30.

   m_z = 2.0*!pi*m_bar

; First compute horizontal wavenumber
   k_bar = fltarr(n_good)
   k_bar = f*m_z(b)*sqrt(f_w(b)^2-1)/n_bar
   l_x = 2.0*!pi/k_bar

; Find intrinsic phase speeds
   c_z = f*f_w(b)/(m_z(b))
   c_i = f*f_w(b)/k_bar
   c_ix = c_i*sin(phi(b))
   c_iy = c_i*cos(phi(b))

; Now compute group velocity c_g = c_i + U
   c_gx = c_ix + u_mm(b)
   c_gy = c_iy + v_mm(b)
;plot_cg,c_gx,c_gy

; Find ground based phase speed, c
; and ground-based frequency
   omega = f*f_w(b) + k_bar*u_mean(b)*cos(theta(b)-phi(b))
   c =  abs((c_i + u_mean(b)*cos(theta(b)-phi(b))))
   c_x = c/sin(phi(b))      ; note division since not true component velocity
   c_y = c/cos(phi(b))
   c_xcomp = (c_i + u_mean(b)*cos(theta(b)-phi(b)))*sin(phi(b))
   c_ycomp = (c_i + u_mean(b)*cos(theta(b)-phi(b)))*cos(phi(b))

   df = df(b)

   return
END                             ; End of phase speed

; postdarkening (Nastrom and VanZandt (2001) p. 14,370)
pro postdark, tsh, m
n=n_elements(m)
j=1.+findgen(n)
tsh=tsh/(2.0*(1-cos(2.0*!pi*j/n)))
return
end
;****************************************************************
FUNCTION pressure,z
; Procedure to produce pressure  profile
; for height range from 18 - 25 km
   zO = 0.250
;Standard Height-Pressure levels for Radiosonde Data at Cocos Island
   hstd = [8.84, 8.77, 8.70, 8.57, 8.32, 8.16,  $
           7.96, 7.83, 7.66, 7.44, $
           7.14, 6.96, 6.85, 6.75, 6.72]
   zstd = [0.100, 0.784, 1.514, 3.157, 5.869,  $
           7.581, 9.686, 10.955, 12.432, $
           14.219, 16.553, 18.603, 20.617, 23.766, 26.389]

   pstd = [1000., 925, 850, 700, 500, 400, 300,  $
           250, 200, 150, 100, $
           70, 50, 30, 20]

   p = fltarr(n_elements(z))
   po = interpol(pstd,zstd,zO)
   po = po(0)
   H = interpol(hstd,zstd,z)
   p = po*exp(-(z-zO)/H)
; Convert pressure to Pascals
   p = p*100.
   return,p
END
PRO mean_spec,u,v,m_bar,m,lamda,navr,cpm
;Procedure to calulate mean vertical-wavenumber for wind components
;m and lamda are the output vertical wavenumber and wavelength arrays
;averaged over navr points
;cpm is the sample spacing in metres
;uspec and vspec are the output arrays (real) of length npts/navr
;Generate window function
;m_bar is the number of mean wavenumbers
   a=size(u)
   npts=a(1)
   n2 = npts/2
   IF (a(0) EQ 2) THEN n_data = a(2)
   m_bar = reform(fltarr(n_data))
   window = welch(npts)
   nred = npts/navr
   nmax=npts-1
   nf = float(npts)/(total(window*window))

   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   IF (navr NE 1) THEN  m = m + delm/2.
   m(0) = delm/2.
   norm = float(navr)*nf/delm

   i = complex(0,1)
   IF (n_data GT 1) THEN BEGIN
      FOR i = 0, n_data-1 DO BEGIN
         uf = (u(0:nmax,i)-total(u(0:nmax,i))/npts)*window
         vf = (v(0:nmax,i)-total(v(0:nmax,i))/npts)*window
         ut = fft(uf, -1)
         us = float(ut*conj(ut))
         vt = fft(vf, -1)
         vs = float(vt*conj(vt))
         us =  us + vs

         if (navr ne 1) THEN  $
          us = rebin(us, nred)*norm  $
         ELSE  $
          us = us*norm

         m_bar(i) = rebin(us(1:n2)*m(1:n2),1)/rebin(us(1:n2),1)
      ENDFOR
   ENDIF
   lamda  = 1.0/(m*1000.0)
   RETURN
END
;*********************************************************************
PRO stokes,u,v,u_m,v_m,theta,n_bar,f_w,df
;*****************************************************
;Procedure to calculate Stokes parameters for vertical
;wavenumber spectra
;*****************************************************
;Fourier transform velocity profiles, assumed to be at
;30 m spacing
; theta is azimuth computed from <u'T90>
   a = size(u)
   n = a(1)
   na = n/2
   loop =a(2)
   z30 = findgen(a(1))*30+18000.

   is = fltarr(na, loop)
   ds = is & ps = is & qs = is & df = is & phi = is
   df = fltarr(loop)
   xd = df & yd = df & phi = df & axr = df
   FOR k = 0, loop -1 DO BEGIN
      ut = fft(u(*, k), -1)
      vt = fft(v(*, k), -1)

;Form Stokes parameters following Eckermann and Vincent (1989)

      it = float(ut*conj(ut) + vt*conj(vt))
      dt = float(ut*conj(ut) - vt*conj(vt))
      pt = 2.0*float(conj(ut)*vt)
      qt = 2.0*imaginary(conj(ut)*vt)

      is(*, k) = it(1:na) & ds(*, k) = dt(1:na)
      ps(*, k) = pt(1:na) & qs(*, k) = qt(1:na)

      df(k)  = sqrt(total(qt(0:na))^2 + total(pt(0:na))^2 +  $
                    total(dt(0:na))^2)/total(it(0:na))
      phi(k) = atan(total(pt), total(dt))/2.

      xi = asin(abs(total(qt(0:na))/(df(k)*total(it(0:na)))))/2.0
      axr(k) = 1.0/tan(xi)
   ENDFOR
; Correct for tranverse shear term
   u_t = fltarr(a(1))
   du_t_dz = fltarr(a(2))
   FOR i = 0,a(2)-1 DO BEGIN
      u_t = u_m(*,i)*cos(theta(i))-v_m(*,i)*sin(theta(i))
      du_t_dz(i) = total(deriv(z30,u_t))/float(a(1))
   ENDFOR
   axr_corr = du_t_dz/n_bar
   f_w = axr-axr_corr
END ; End Stokes
;*************************************************************
PRO phase_speed,u_m,v_m,phi,up,vp,f,n_bar,f_w,m_bar,k_bar, $
                omega,c_z,c_i,c_x,c_y,df,c_ix,c_iy,c_gx,c_gy, $
;               c_xcomp,c_ycomp
                c_xcomp,c_ycomp, u_mean, u_mm, v_mm, theta
; Procedure to compute phase speeds
   a = size(up)
   b = where(f_w GT 1 AND f_w LE 10, n_good)
;compute azimuth of mean winda = size(up)
   u_mm = reform(rebin(u_m,1,a(2)))
   v_mm = reform(rebin(v_m,1,a(2)))
   theta = atan(u_mm,v_mm)
   u_mean = sqrt(u_mm^2+v_mm^2)
   mean_spec,up,vp,m_bar,m,lz,1,30.

   m_z = 2.0*!pi*m_bar

; First compute horizontal wavenumber
   k_bar = fltarr(n_good)
   k_bar = f*m_z(b)*sqrt(f_w(b)^2-1)/n_bar
   l_x = 2.0*!pi/k_bar

; Find intrinsic phase speeds
   c_z = f*f_w(b)/(m_z(b))
   c_i = f*f_w(b)/k_bar
   c_ix = c_i*sin(phi(b))
   c_iy = c_i*cos(phi(b))

; Now compute group velocity c_g = c_i + U
   c_gx = c_ix + u_mm(b)
   c_gy = c_iy + v_mm(b)
;plot_cg,c_gx,c_gy

; Find ground based phase speed, c
; and ground-based frequency
   omega = f*f_w(b) + k_bar*u_mean(b)*cos(theta(b)-phi(b))
   c =  abs((c_i + u_mean(b)*cos(theta(b)-phi(b))))
   c_x = c/sin(phi(b))      ; note division since not true component velocity
   c_y = c/cos(phi(b))
   c_xcomp = (c_i + u_mean(b)*cos(theta(b)-phi(b)))*sin(phi(b))
   c_ycomp = (c_i + u_mean(b)*cos(theta(b)-phi(b)))*cos(phi(b))

   df = df(b)

   return
END                             ; End of phase speed
;************************************************
PRO angular_spec,phi,en,title,mean_dir
; Procedure to plot angular spectrum in polar form
; First compute histogram of directions
; Phi assumed to be clockwise from north
; En is the wave energy for each profile
   dir = phi*!radeg
   b = where(dir lt 0,n_dir)
   IF (n_dir GT 0) THEN dir(b)=dir(b)+360.

   r_d = histogram(dir,bin = 30,min = 0,max = 360,reverse_indices = h)
   a = size(r_d)
   r = fltarr(a(1))
   theta = findgen(13)*30*!dtor

; h gives indices of elements in each bin
; e_tot is the total energy for the period under consideration
   e_tot = total(en)
   FOR i = 0,11 DO BEGIN
      IF (r_d(i) NE 0) THEN BEGIN
         v = h(h(i):h(i+1)-1)
         r(i) = total(en(v))/e_tot ;Angular spectrum
      ENDIF ELSE BEGIN
         r(i) = 0
      ENDELSE
   ENDFOR
 goto,jump4
   !x.style = 1
   !y.style = 1
   !x.range = [-0.5,0.5]
   !y.range = [-0.5,0.5]
   !x.tickv = [-0.5,-0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3,0.4, 0.5]
   !x.tickname = ['!170.4','0.2', ' ', '0.2', '0.4']
   !y.tickv = [ -0.5 ,-0.4,-0.3,-0.2,-0.1, 0.0, 0.1, 0.2, 0.3,0.4, 0.5]
   !y.tickname = ['0.4','0.2',' ','0.2','0.4']
   df = 30.0*!dtor
;  the array atheta allows the plotting in polar co-ords to
; plot with N to top of page, and go clockwise in angle
   atheta = !pi*.5 - theta
   b = where(atheta lt 0.)
   atheta(b) = atheta(b) + 2.*!pi
   plot,r,atheta,xst = 5,yst = 5,/polar,/nodata,$
    title = title,charsize = 1.5 ,$
    xmargin = [5,5]
   oplot,[0,r(0)],[atheta(0),atheta(0)],/polar
   oplot,[0,r(0)],[atheta(0)-df,atheta(0)-df],/polar
   arc_circ,r(0),atheta(0),-df
   FOR i = 1,11 DO BEGIN
      oplot,[0,r(i)],[atheta(i),atheta(i)],/polar
      oplot,[0,r(i)],[atheta(i)-df,atheta(i)-df],/polar
      arc_circ,r(i),atheta(i),-df
   ENDFOR
   axis,0,0,xax = 0,charsize = 1.3
   axis,0,0,yax = 0,charsize = 1.3
   xyouts,0.495,0.02,'E',charsize = 1.0
   xyouts,0.015,0.45,'N',charsize = 1.0
; Reset plot parameters
   resetplt,/all
jump4:
; Compute mean direction weighted by energy
   mean_vec = [total(en*sin(phi)), total(en*cos(phi))]
   mean_dir = atan(mean_vec(0), mean_vec(1))*!radeg
   if mean_dir LT 0 THEN mean_dir = mean_dir + 360.	;my unders deg,from east
   return
END                             ; end angular_spec
;************************************************************
;PRO directions,up,vp,tp,rho,phi,ut,vt,uq,ui
PRO directions,up,vp,tp,rho,phi,ut,vt,uq,vq,ui,vi	;newly modified
; Procedure to compute mean direction of wave propagation
; from velocity and normalized temperature perturbations.
; Use covariances <u'T'+90> and <v'T'+90> to determine
; azimuth from North. Where T'+90 is the value of
; temperature after shifting phase by +90 deg via Hilbert
; transform.

   a = size(up)
   phi = fltarr(a(2))					;dir of wave propagation
   ut = phi & vt = phi
   uq = ut & ui = ut
   vq = ut						;newly added
   loop = a(2)-1					;number of profiles
   FOR k = 0, loop DO BEGIN
; Carry out Hilbert transform
      to = float(HILBERT(tp(*,k), -1))

; Low-pass filter the temperature to match smoothing
; inherent in the wind profiles (~300 m trangular weighted smoothing
; with Australian data)
      to = smooth(to, 5)
      ti = smooth(tp(*,k),5)    ; Untransformed temp
      x = total(to*up(*,k)*rho(*,k))/float(a(1))	;column average
      y = total(to*vp(*,k)*rho(*,k))/float(a(1))	;column average
      ut(k) = x
      vt(k) = y
      uq(k) = total(to*up(*,k))/n_elements(to)
      vq(k) = total(to*vp(*,k))/n_elements(to)		;newly added
      ui(k) = total(ti*up(*,k))/n_elements(ti)
; Phi is azimuth from north
      phi(k) = atan(x, y)
   ENDFOR
   return
END                             ; End Directions
;*********************************************************
PRO tspec_plot, ts, m,lamda
   a = size(ts)
   n = a(1)/2-10
   plot_oo,m(1:n),ts(1:n),xstyle = 9, $
    xmargin =[15,0],$
    xtitle='!17WAVENUMBER (cpm)',$
    ytitle='!17Normalized Temperature PSD (cpm!E-1!N)',/NODATA
   oplot,m(1:n),ts(1:n)
   axis,xaxis=1,xstyle = 1, $
    xrange=[lamda(1), $
            lamda(n)],xtitle='WAVELENGTH (km)'
   return
END
;*************************************************
PRO t_spec,t,tspec,err,m,lamda,navr,cpm
; Procedure to calulate vertical-wavenumber power spectrum for temperature
; m and lamda are the output vertical wavenumber and scale arrays
; averaged over navr points
; cpm is the sample spacing in metres
; tspec is the output array (real) of length npts/navr
; err is a standard deviation of the tspec at each wavenumber
; Generate window function
; Average over all available observations if necessary
   a=size(t)
   npts=a(1)
   IF (a(0) EQ 2) THEN n_obs = a(2) $
    ELSE n_obs = 1
   window = welch(npts)
   nred = npts/navr
   ts = fltarr(npts)
   tsq =fltarr(npts)
   nmax=npts-1
   nf = float(npts)/(total(window*window))

   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   if (navr ne 1) then m = m + delm/2.		; ? my question
   m(0) = delm/2.
   FOR i = 0,n_obs-1 DO BEGIN
      uf = complex((t(0:nmax,i)-total(t(0:nmax,i))/npts)*window ,0.0)
      ut = fft(uf,-1)
      spec = float(ut*conj(ut))
      ts = ts +spec
      tsq =spec*spec+tsq
   ENDFOR
   fnp =float(n_obs)
   norm = float(2*navr)*nf/(n_obs*delm) ; NB One-sided spectrum
   err = tsq/fnp - ts*ts/(fnp*fnp)
   err = fnp*sqrt(err)
   tspec = rebin(ts,nred)*norm
   tspec = tspec(0:npts/2)
   err = rebin(err,nred)*norm
   err = err(0:npts/2)
   lamda = 1.0/(m*1000)
return
END ; t_spec
;*********************************************************************
PRO rotary_spec,u,v,acp,ccp,m,lamda,navr,cpm
;Procedure to calulate vertical-wavenumber power spectrum for wind components
;m and lamda are the output vertical wavenumber and wavelength arrays
;averaged over navr points
;cpm is the sample spacing in metres
;uspec and vspec are the output arrays (real) of length npts/navr

;Generate window function
   a=size(u)
   npts=a(1)
   n2 = npts/2
   IF (a(0) EQ 2) THEN n_data = a(2) ELSE n_DATA =1
   window = welch(npts)
   nred = npts/navr
   nmax=npts-1
   nf = float(npts)/(total(window*window))
   delm = 1.0/(cpm*float(nred))
   m = findgen(nred)*delm
   IF (navr NE 1) THEN m = m + delm/2.
   m(0) = delm/2.
   norm = float(navr)*nf/delm
   acp = fltarr(n2) & ccp = acp

   FOR i = 0,n_data-1 DO BEGIN
      uf = (u(0:nmax,i)-total(u(0:nmax,i))/npts)*window
      vf = (v(0:nmax,i)-total(v(0:nmax,i))/npts)*window
      ut = fft(complex(uf,vf), -1)
      us = float(ut*conj(ut))
      IF (navr NE 1) THEN  $
       us = rebin(us,nred)*norm ELSE us = us*norm
;Anticlockwise component is positive half space
;clockwise component is negative half space
      acp = us(1:n2)+acp
      ccp = rotate(us(n2:nmax),2)+ccp
   ENDFOR
   acp = acp/float(n_data)
   ccp = ccp/float(n_data)
   lamda  = 1.0/(m*1000.0)
   return
END                             ; End rotary_spec
;*********************************************************************
PRO constants,lat,n_bar,f,bo,co,wbar1,wbar2,wbar1p,deltaw	;I add this
; Procedure to compute spectral constants
; based on Fritts and VanZandt, JAS, 1993.
; lat = station latitude in degrees
; n_bar = mean brunt (stability) frequency

   latt = abs(lat)
   inertial_period = 12./sin(latt*!dtor)
   f = 2.0*!pi/(3600.0*inertial_period)

   f_hat = f/n_bar
   p = 5./3.                    ; spectral slope of frequncy spectrum
   q = (p-1.)
   r = (2.-p)
   s = (p+1.)
   Bo = q*f^q/(1.-f_hat^q)
   Co = (f^(-q))*((1.-f_hat^q)/q - (1.-f_hat^s)/s)/(1.-f_hat^2)
; Compute mean frequency for canonical spectrum
; For p= 5/3
   p = 5./3.
   wbar1 = (q/r)*n_bar*(f_hat^q)*(1-f_hat^r)		;eq. (16) of VAE97
   wbar1p = (q/r)*n_bar*(f_hat^q)*(1-f_hat^(-r))	;I add this
   deltaw=1-f*f/wbar1p/wbar1p				;I add this
   wbar2 = -f*alog(f_hat)				;eq. (17) of VAE97
   return
END

;*********************************************************
PRO fit, ts,sigma,m,a,eo,ms,t
; Procedure to fit m-spectrum for normalized temperature spectrum (ts)
; to modified Desaubies spectrum in vertical wavenumber (m)

   dummystring = ' '
   npt = n_elements(m)          ; Make spectrum one-sided
   n = npt/2.-1
   s = ts(1:n)
   x = m(1:n)
   ss = sigma(1:n)
; Make initial guess of fitting constants
; Get mean-square normalized temperature
   dm = m(4)-m(3)
   ts_bar = total(s)*dm
; Next mean wavenumber
   m_bar = total(s*x)*dm/ts_bar
; First guess at m_star
   ms = x(1)
   fo = ts_bar/ms
   t = 4.0
   a = [fo,ms,t ]
   fa = {X:x, Y:s, ERR:ss}
   functc,x,a,f        ; f is starting model
   deviates = (s-f)
; fitting a model to the avaerage spectrum using fitting algorithm
; embodied in mpfit.pro
   p_fit = mpfit('mp_funct',a,functargs= fa,/QUIET)
   functc,x,p_fit,spec_fit      ; evaluate fitted function
;loadct,40
;   Oplot,x,spec_fit,line = 1,color=240    ; plot it over data
;loadct,0
   a = p_fit
   return
END
;created on 5/14/2002

PRO functc2,x,a,f,pder
;
; I add this
;
; Return a function value in f.
; based on lmfunct
; Function for fitting modified Desaubies spectrum
; 23 June 1998 RAV
; F = Ao mu/(1+mu^A2)
; where mu = x/A1

;
;a(0)=F_0
;a(1)=m_*
;a(2)=t+1
;
common fit6,t6_0
   mu = x/a(1)				;m/m*
;  d = mu^a(2)				;(m/m*)^(t+1)
   d = mu^(t6_0+1.0)
   b = 1./(1+d)
   c = mu*b
   f = a(0)*c				;f0 (m/m*) / (1+(m/m*)^(t+1))
   IF (n_params() GE 4) THEN $
    pder = [ [f/a(0)],  $
             [-f*b*(1+(1-(t6_0+1.0))*d)/a(1)] ]
   return
END

FUNCTION mp_funct2, p,X=x,Y=y,ERR=sigma
;
; I add this
;
; this function provided to be called by the mpfit.pro
; routine . Devised Aug 12 1998 AC Beresford , Atmos Phys Univ of Adelaide
   nofx = n_elements(x)
   model = fltarr(nofx)
   deriv =fltarr(nofx)
;  functc, x,p,model
   functc2, x,p,model
   deriv = (y-model)/sigma
   return, deriv
END

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

FUNCTION Welch2,n
;similar to welch but with minor difference (Num Recipes in C, p 547)
;Procedure for calculating Welch Window function (Num Recipes, p 422)
j = findgen(n)
n2=n/2.
RETURN, 1. - ((j - n2)/n2)^2
END ; End Welch

;+++++++++++++++++++++++++++++++++++++++++++++++++++++++
;--> nht (number of levels for a hrrd profile)
function get_eclipse_nht,fname

nht=0
blank = ' '
header = ' '

close,1
openr,1,fname
on_ioerror, break               ;IF I/O ERROR GO TO BREAK

for j = 1, 20 do readf,1,blank

;NOW READ IN DATA, SAVING DATA WHEN END OF FILE IS ENCOUNTERED
i = 0
repeat begin
    readf,1,header
    i=i+1
endrep until eof(1)
nht=i

break:   close,1
return,nht
end
;+++++++++++++++++++++++++++++++++++++++++++++++++++++++
;
pro gw_analysis2,up $			;zonal wind perturbation (m/s)
               ,vp $			;meridional wind perturbation (m/s)
	       ,arp $			;ascending rate perturbation (m/s)
               ,tp $			;temperature perturbation (K)
               ,um $			;mean zonal wind (m/s)
               ,vm $			;mean meridional wind (m/s)
	       ,arm $			;mean ascending rate (m/s)
               ,tb $			;mean temperature (K)
               ,pr $			;pressure (hpa)
               ,lat $			;latitude (deg)
               ,lon $			;longitude (deg)
               ,zkm $			;vertical grid (km)
               ,dz $			;vertical grid resolution (km)
               ,ipw $			;0 no prewhitening; 1 prewhitening
               ,iw $			;0 old method; 1 new method
               ,id $			;0 no linear detrend; 1 linear detrend
               ,ke,kez,kev,kevert,pe,f_w,m_bar,up_frac,mean_dir,uw,vw $ ;output
               ,n_bar=n_bar,ttl=ttl

common fit6,t6_0
nnn=n_elements(zkm)
;dz=zkm(1)-zkm(0)
dzm=dz*1000.
zm=zkm*1000.
z = zkm
p = pr*100.
p_r = p/287.05

tph = tp/tb
tph2=tph				;I add this
dt = fltarr(nnn)
dt = deriv(tb)/dz 			; Temperature gradient K/km
n_sq = (dt+9.8)*9.8/(tb*1000.)
n_bar = sqrt(avg1d(n_sq))

constants,lat,n_bar,f,bo,co,w1,w2,w1p,deltaw	;I add this

; mean square value of normalized temperature perturbation
tps_bar =avg1d(tph^2)
;print,'ok3'

;linear detrend tph
if id eq 1 then begin
    tphp=tph
    detrend, tphp, z, 1
    tph2=tphp
endif

;prewhitening
if ipw eq 1 then begin
    tph2=tph(1:nnn-1)-tph(0:nnn-2)
endif

; Compute average spectrum
;print,'ok3a'
if iw eq 0 then t_spec_new,tph2,tsh,terr,m,lamda,1,dzm
;print,'ok3b'
if iw eq 1 then t_spec2,tph2,tsh,terr,m,lamda,1,dzm
;print,'ok3c'
;stop,'666'

; postdarkening
if ipw eq 1 then postdark, tsh, m

; Modify spectrum for response time
;tsh = tsh*(1+(40*m*2*!pi)^2)
; modify error estimates as well
; added 18 aug 1998 AC Beresford atmos phys Adelaide
;terr = terr*(1+(40*m*2*!pi)^2)


; Compute wind perturbations.
; Average over central part of spectrum to avoid end effects
n1 = 5
n2 = nnn-6

upg = up(n1:n2)
vpg = vp(n1:n2)
arpg = arp(n1:n2)
umg = um(n1:n2)
vmg = vm(n1:n2)
armg = arm(n1:n2)
tpg = tp(n1:n2)/tb(n1:n2)
ke = 0.5*avg1d(upg^2+vpg^2)
pe = 0.5*avg1d((9.8*tpg/n_bar)^2)
en = ke+pe
et = en
tbg = tb(n1:n2)
kez = 0.5*avg1d(upg^2)
kev = 0.5*avg1d(vpg^2)
kevert = 0.5 * avg1d(arpg^2)
eo = tps_bar/(bo*co)*(9.8/n_bar)^2
;stop,'222'

; Compute density profile
p_rg = p_r(n1:n2)
rho=p_rg/tbg


; Compute fraction of upgoing energy.
; In southern hemisphere upgoing waves have
; anticlockwise polarisation (acp)
; In northern hemisphere use clockwise component (ccp).
rotary_spec,upg,vpg,acp,ccp,m,lamda,1,dz*1000.
IF (lat LT 0) THEN  $
    up_frac = total(acp)/total(acp+ccp) $
ELSE  $
    up_frac = total(ccp)/total(acp+ccp)

; Compute mean direction of propagation
directions_new,upg,vpg,tpg,rho,phi,ut,vt,uq,vq,ui,vi	;newly modified

;plot the angular distribution and calculate mean_dir
dir = phi*!radeg
IF dir lt 0 THEN dir=dir+360.
mean_dir=dir

;print,'ok7'
; Compute density-weighted momentum fluxes
; following Vincent et al (1996)
fac = 9.8/n_bar^2
uw = fac*w1*ut			;energy weighted flux
vw = fac*w1*vt			;energy weighted flux
uw2 = fac*w1*uq			;newly added
vw2 = fac*w1*vq			;newly added
uwp = -fac*w1p*ut*deltaw	;newly added
vwp = -fac*w1p*vt*deltaw	;newly added
uw2p = -fac*w1p*uq*deltaw	;newly added
vw2p = -fac*w1p*vq*deltaw	;newly added

; Compute mean frequency
stokes_new,upg,vpg,umg,vmg,phi,n_bar,f_w,df,zm(n1:n2)

if iw eq 0 then phase_speed_new,umg,vmg,phi,upg,vpg, $
    f,n_bar,f_w,m_bar,k_bar,omega,c_z,c_i,c_x,c_y,df, $
    c_ix,c_iy,c_gx,c_gy,c_xcomp,c_ycomp, u_mean, u_mm, v_mm, theta,dzm
if iw eq 1 then phase_speed2,umg,vmg,phi,upg,vpg, $
    f,n_bar,f_w,m_bar,k_bar,omega,c_z,c_i,c_x,c_y,df, $
    c_ix,c_iy,c_gx,c_gy,c_xcomp,c_ycomp, u_mean, u_mm, v_mm, theta

;save,filename=outflname, $
;    w1,w2,f,ke,pe,phi,ut,vt,f_w,df,n_bar,m_bar,k_bar, $
;    omega,c_z,c_i,c_x,c_y,c_ix,c_iy,c_gx,c_gy,kez,kev, $
;    sez,en,se,c_xcomp,c_ycomp,month,et,lat,lon,eo, $
;    up_frac,uw,vw,mean_dir,uq,vq,ui,acp,ccp,type,ms,t,u_mean, $
;    theta,u_mm,v_mm, $
;    uw2,vw2,notes,t2,ms3,t3,t4,t5,ms6,ms7,ms8,ms9,ms10,t10,ms11, $
;    uwp,vwp,uw2p,vw2p
;save,filename=outflname,ke,kez,kev,pe,f_w,m_bar,up_frac,mean_dir,uw,vw,notes,k_bar,lat
;print,'ok11'

return
end

;********************************************
;CALCULATE THE COROLIOS PARAMETER FROM LATITUDE
;APPLICABLE TO BOTH SCALAR AND ARRAY OF LATITUDES
function get_coriolis, latitude ;LATITUDE, IN DEG
omega = 7.2919996d-05
f = 2.0d*omega*sin(latitude*!dtor)
return, f
end

;********************************************
function dispersion_m_w_to_k,w,m,lat $
                            ,n=n,hrou=hrou,help=help
;( INTRINSIC FREQUENCY, VERTICAL WAVENUMBER) ==> HORIZONTAL WAVENUMBER
;----------------------------------------------
if keyword_set(help) then begin
    print,''
    print,'Purpose: '
    print,'         ( intrinsic frequency + vertical wavenumber)'
    print,'                 --> horizontal wavenumber'
    print,'Usage: '
    print,'         k=dispersion_m_w_to_k(w,m,f,n=n,alpha=alpha)'
    print,'Steps:'
    print,'         '
    print,'Input:'
    print,'         w -- intrinsic frequency [SI]'
    print,'         m -- vertical wavenumber [SI], 2*!PI / Lz'
    print,'         lat -- latitude [deg]'
    print,'Keywords:'
    print,'         help -- print this information'
    print,'         n -- Brunt-Vasalla freq [SI]'
    print,'         hrou -- density scale height [km]'
    print,'Output:'
    print,'         k -- horizontal wavenumber [SI], 2*!PI / Lh'
    print,'Examples:'
    print,'         '
    print,'History:'
    print,'         08/11/2006 created by Jie Gong'
    print,'Note:'
    print,'         '
    print,''
    stop
endif
;----------------------------------------------
if ~ keyword_set(hrou) then hrou=7.
if ~ keyword_set(n) then n=0.02                 ;typical stratospheric value
alpha=0.5/(hrou*1.e3)
f=get_coriolis(lat)
k=sqrt((w*w-f*f)/(n*n-w*w)*(m*m+alpha*alpha))
;----------------------------------------------
return,k
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;c

function gw_analysis_struct,input,plot=plot,ttl=ttl,help=help
;----------------------------------------------
if keyword_set(help) then begin
    print,''
    print,'Purpose: '
    print,'         do the GW analysis following VAE97'
    print,'Usage: '
    print,'         gw=gw_analysis_struct(input)'
    print,'Steps:'
    print,'         '
    print,'Input:'
    print,'         input -- the input structure'
    print,'             .up : zonal wind perturbation [m/s]'
    print,'             .vp : meridional wind perturbation [m/s]'
    print,'		.arp: ascending rate perturbation [m/s]'
    print,'             .tp : temperature perturbation [K]'
    print,'             .um : mean zonal wind [m/s]'
    print,'             .vm : mean meridional wind [m/s]'
    print,'		.arm: mean ascending rate [m/s]'
    print,'             .tm : mean temperature [K]'
    print,'             .pm : mean pressure [hpa]'
    print,'             .lat : latitude location [deg]'
    print,'             .lon : longitude location [deg]'
    print,'             .z : vertical grid [km]'
    print,'             .dz : vertical grid resolution [km]'
    print,'             .ipw : 0 no prewhitening; 1 prewhitening'
    print,'             .iw : 0 old method; 1 new method'
    print,'             .id : 0 no linear detrend; 1 linear detrend'
    print,'Keywords:'
    print,'         help -- print this information'
    print,'         plot -- make preliminary plot'
    print,'         ttl -- title of the preliminary plot'
    print,'Output:'
    print,'         gw -- all the GW info. derived from this analysis'
    print,'               see my dissertation or VAE97 for more details'
    print,'             .ke : kinietic energy density [SI]'
    print,'             .kez : zonal kinietic energy density [SI]'
    print,'             .kev : meridional kinietic energy density [SI]'
    print,'             .pe : potential energy density [SI]'
    print,'             .f_w : intrinsic frequency/f'
    print,'             .m_bar : reciprocal of vertical wavelength [SI]'
    print,'             .up_frac: fraction of upward propagating waves'
    print,'             .mean_dir : mean propagation direction [deg]'
    print,'                         azimuth from north (?)'
    print,'             .uw : zonal flux [?]'
    print,'             .vw : meridional flux [?]'
    print,'             .n_bar : buoyancy frequency [SI]'
    print,'             .lz: vertical wavelength [km]'
    print,'             .lh: horizontal wavelength [km]'
    print,'             .m: vertical wavenumber, m=2*Pi*m_bar [SI]'
    print,'             .f: Coriolis parameter [SI]'
    print,'             .lat: latitude [deg]'
    print,'             .omega: intrinsic frequency [SI]'
    print,'             .k: horizontal wavenumber [SI]'
    print,'             .kx: zonal wavenumber [SI]'
    print,'             .ky: meridional wavenumber [SI]'
    print,'             .input: input to calculate the gw para.'
    print,'		.kevert: vertical kinetic energy density [SI]'
    print,'Note:'
    print,'         virtually the same as gw_analysis2, except to make the'
    print,'         code more reader friendly and easier to use'
    print,''
    stop
endif
;----------------------------------------------
gw_analysis2,input.up,input.vp,input.arp $
	    ,input.tp,input.um,input.vm,input.arm $
            ,input.tm,input.pm,input.lat[0],input.lon[0] $
            ,input.z,input.dz,input.ipw,input.iw,input.id $
            ,ke,kez,kev,kevert,pe,f_w,m_bar,up_frac,mean_dir,uw,vw $
            ,n_bar=n_bar,ttl=ttl
;----------------------------------------------
lz=1.e-3/m_bar					;[km]
m=2.*!pi*m_bar					;2*!PI / Lz instead of 1/Lz
lat=input.lat[0]					;[deg]
f=get_coriolis(lat)
omega=f_w*f					;intrinsic frequency [SI]

k=dispersion_m_w_to_k(omega,m,lat,n=n_bar,hrou=7.)
lh=2.e-3*!pi/k					;horizontal wavelength [km]
phi2kl,mean_dir,lh,kx,ky
gw={ke:ke,kez:kez,kev:kev,kevert:kevert,pe:pe,f_w:f_w,m_bar:m_bar,$
    up_frac:up_frac, $
    mean_dir:mean_dir,uw:uw,vw:vw,n_bar:n_bar, $
    lz:lz,lh:lh,m:m,f:f,lat:lat,omega:omega,k:k,kx:kx,ky:ky,input:input,$
    outputflag:0}
;----------------------------------------------
return,gw
end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; PURPOSE : cal. the perturbations using a selected method for one sounding
;
; INPUT :
;
; OUTPUT :
;
; ALGORITHM :
;
; NOTES : created on 1/26/2004
;
;         modified on 4/6/04 to make the code more efficient
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro perturb_hrrd $

               ;input
               ,u $			;u interpolated to regular grid
               ,flag $			;0: enough valid data; 1: not enough
               ,npoly=npoly $		;order of polynomial fit
               ,flow=flow $		;lower limit of the high-pass filter
               ,fhigh=fhigh $		;upper limit of the low-pass filter

               ;output
               ,up $			;perturbation, same unit as the input
               ,ub			;background, same unit as the input

if flag eq 1 then return

;polynomial fit
if keyword_set(npoly) then begin
    co=poly_fit(double(findgen(n_elements(u))),double(u),npoly,ub)
    up=u-ub
    return
endif
;high-pass filter --> perturbation
if keyword_set(flow) then begin
    up=digital_smooth(u,flow,1)
    ub=u-up
    return
endif
;low-pass filter --> background
if keyword_set(fhigh) then begin
    ub=digital_smooth(u,0,fhigh)
    up=u-ub
    return
endif

end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; PURPOSE : obtain the raw data info. (data, missing, code) for one radiosonde
;
; INPUT : name of radiosonde profile (fname)
;
; OUTPUT : data,missing,code
;
; ALGORIGHM :
;
; NOTES : more complete than read_whole_profile.pro
;
; missing data flag: 	P	mb	9999.0
;			T	c	999.0
;			U	m/s	9999.0
;			V	m/s	9999.0
;			AR	m/s	999.0
;			Z	m	99999.0
;          see the more complete in missing
;
;HISTORY: change read_hrrd to read_eclipse to handle eclipse balloon sounding
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;c

pro read_eclipse $

    ;INPUT
    ,fname $			;name of the Sounding
    ,fast=fast $		;if set, faster but larger strcuture
				;also there may be zero paddings
				;so it's better not to use this option

    ;OUTPUT
    ,data $			;data
    ,nrec $			;record length
    ,missing $			;missing data info.
    ,code			;quality control info.

;--> nht
if ~ keyword_set(fast) then begin
    nht=get_eclipse_nht(fname)-10 ;with newly processed data, the last 10 lines dedicated to header (should be flexible to adapt different headers)
endif else begin
    nht=10000			;MAX POSSIBLE NUMBER OF OBS. FOR ONE PROFILE
endelse

data = {tm:fltarr(nht), $	;Time			s	9999.0  #required
        p:fltarr(nht), $	;Pressure		hPa	9999.0   #required
        t:fltarr(nht), $	;Dry-bulb temp		C	999.0   #required
        rh:fltarr(nht), $	;Relative Humidity	%	999.0   #optional, not used
        ws:fltarr(nht), $	;Wind Speed		m/s	999.0   #required
        dir:fltarr(nht), $	;Wind Direction		deg	999.0   #required
        lon:fltarr(nht), $	;Longitude		deg	999.0   #required
        lat:fltarr(nht), $	;Latitude		deg	999.0   #required
        z:fltarr(nht), $	;Altitude		m	99999.0 #required
	gph:fltarr(nht),$	;Geopotential Hgt	m	99999.0 #optional, not used
	mri:fltarr(nht),$	;??			C	999.0	#not used
	ri:fltarr(nht),$	;??			C	999.0   #not used
        tdew:fltarr(nht), $	;Dew Point		C	999.0   #not used
        tvir:fltarr(nht), $	;Virt. temp		C	999.0   #not used
	rs:fltarr(nht),$	;Rising speed		m/s	999.0   #required (can be calculated using doi:10.1175/2008JTECHA1240.1)
	;//to Oswego team: some radiosonde profile doesn't provide rs as default output. Maybe it's good to come up with
	;//a function to calculate it out for users using the paper listed here. If too much trouble, let's require user to input that.

        ele:fltarr(nht), $	;Elevation Angle	deg	999.0   #not used
        azi:fltarr(nht), $	;Azimuth		deg	999.0   #not used
	range:fltarr(nht),$	;			m	999.0   #not used
	D:fltarr(nht),$		;			kg/m3 	999.0   #not used
	u:fltarr(nht),$		;u wind,derived 	m/s	999.0   #not input;calculated from ws and wdir
	v:fltarr(nht)$		;u wind,derived 	m/s	999.0   #not input;calculated from ws and wdir
	}
missing = {tm:9999.0, $
           p:9999.0, $
           t:999.0, $
           rh:999.0, $
           ws:999.0, $
           dir:999.0, $
           lon:999.0, $
           lat:999.0, $
           z:99999.0, $
           gph:99999.0, $
           mri:999.0, $
           ri:999.0, $
           tdew:999.0, $
           tvir:999.0, $
           rs:999.0, $
           ele:999.0, $
           azi:999.0, $
           range:999.0, $
           D:999.0, $
	   u:999.0, $
	   v:999.0 $
           }
;code='99.0    Unchecked;'+ $
;     '1.0     Checked (Good);'+ $
;     '2.0     Checked (Maybe);'+ $
;     '3.0     Checked (Bad);'+ $
;     '4.0     Checked (Estimated);'+ $
;     '9.0     Checked (Missing)'
;

blank = ' '
header = ' '

close,1
openr,1,fname
on_ioerror, break		;IF I/O ERROR GO TO BREAK

for j = 1, 20 do readf,1,blank

;NOW READ IN DATA, SAVING DATA WHEN END OF FILE IS ENCOUNTERED
i = 0
iii = 0
repeat begin
    readf,1,header
    iii=strsplit(header,count=c)
    if c NE 19 then goto,stop_reading
    data.tm(i)=float(strmid(header,iii(0),iii(1)-iii(0)))
    data.p(i)=float(strmid(header,iii(1),iii(2)-iii(1)))
    data.t(i)=float(strmid(header,iii(2),iii(3)-iii(2)))
    data.rh(i)=float(strmid(header,iii(3),iii(4)-iii(3)))
    data.ws(i)=float(strmid(header,iii(4),iii(5)-iii(4)))
    data.dir(i)=float(strmid(header,iii(5),iii(6)-iii(5)))
    data.lon(i)=float(strmid(header,iii(6),iii(7)-iii(6)))
    data.lat(i)=float(strmid(header,iii(7),iii(8)-iii(7)))
    data.z(i)=float(strmid(header,iii(8),iii(9)-iii(8)))
    data.gph(i)=float(strmid(header,iii(9),iii(10)-iii(9)))
    data.mri(i)=float(strmid(header,iii(10),iii(11)-iii(10)))
    data.ri(i)=float(strmid(header,iii(11),iii(12)-iii(11)))
    data.tdew(i)=float(strmid(header,iii(12),iii(13)-iii(12)))
    data.tvir(i)=float(strmid(header,iii(13),iii(14)-iii(13)))
    data.rs(i)=float(strmid(header,iii(14),iii(15)-iii(14)))
    data.ele(i)=float(strmid(header,iii(15),iii(16)-iii(15)))
    data.azi(i)=float(strmid(header,iii(16),iii(17)-iii(16)))
    data.range(i)=float(strmid(header,iii(17),iii(18)-iii(17)))
    data.D(i)=float(strmid(header,iii(18),strlen(header)-iii(18)))
    i=i+1

endrep until eof(1)

break: close,1
stop_reading:
nrec=i

data.u(0:nrec-1)=data.ws(0:nrec-1)*sin((data.dir(0:nrec-1)-180.)/180.*!pi)
data.v(0:nrec-1)=data.ws(0:nrec-1)*cos((data.dir(0:nrec-1)-180.)/180.*!pi)

return
end
;CREATE AN MONOTONIC INCREASING ARRAY OF increment dy, WITH MIN Y0, MAX Y1
function make_array3, y0, y1, dy $
                    ,loose=loose $	;not strict about integral multiples
                    ,count=count
on_error,2
if y0 ge y1 then begin
    if y0 gt y1 then message,'Error: y0 should be no bigger than y1' else y=y0
endif else begin
    n=long((y1-y0)/float(dy)+1.1)
    y = fltarr(n)
    y = y0+findgen(n)*dy
    if (abs(y(n-1)-y1) gt 0.1*dy) and $
       (not keyword_set(loose)) then message,'Error: dy not intergral increment'
endelse
count=n_elements(y)
return, y
end
pro check_hrrd_gap $

                  ;input
                  ,zraw $	;raw z data
                  ,uraw $	;raw u data (input/output)
                  ,m_z $	;missing flag for z
                  ,m_u $	;missing flag for u
                  ,z0 $		;bottom z (m)
                  ,z1 $		;top z (m)
                  ,z0p $	;extended z0 (m)
                  ,z1p $	;extended z1 (m)
                  ,note $	;descriptive note on the file being analyzed
                  ,madz=madz $	;if set, the maximum allowed valud of gap (m)
				;default=1 km
                  ,bndy=bndy $	;if set, the maximum gap in the boundary (m)
				;default=0 km

                  ;output
                  ,flag $	;0: enough data; 1: not enough data
                  ,z_out $ 	;selected z
                  ,u_out 	;selected u

;(0) predefine some variables
flag=0	;0: enough data, ub,up successfully retrieved ;1: not enough data
if not keyword_set(madz) then madz=1000.
if not keyword_set(bndy) then bndy=0.
z=zraw
u=uraw

;(1) pick up z,u that correspond to where z and u are not missing
ava=where(z ne m_z and u ne m_u,nava)
if nava eq 0 then begin
    print,note+' No data at all'
    flag=1
    return
endif
z=z(ava)
u=u(ava)
;(2) pick up z,u where z is within the extended range [z0p,z1p]
ava=where(z ge z0p and z le z1p,nava)
if nava eq 0 then begin
    print,note+' No data within the extended altitude range'
    flag=1
    return
endif
z=z(ava)
u=u(ava)
;(3) check the boundaries, if ztop .le. z1-1km or zbot .ge. z0+1km, return
if max(z) le z1-bndy or min(z) ge z0+bndy then begin
    print,note+' Not enough boundary coverage'
    flag=1
    return
endif
;(4) sort z so that z is in ascending order, excluding same level data
ava=uniq(z,sort(z))
nz=n_elements(ava)
nz0=n_elements(z)
;if nz ne nz0 then begin
;    print,note+' has '+string2(nz0-nz)+' same-z data removed'
;endif
z=z(ava)
u=u(ava)
;(5) check the data gap inside, if larger than 1 km, return
ddzz=z(1:nz-1)-z(0:nz-2)
if max(ddzz) ge madz then begin
    print,note+' Too large data gap inside'
    flag=1
    return
endif

u_out=u
z_out=z
return
end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; PURPOSE : interpolate the hrrd data into regular grid
;
; INPUT :
;
; OUTPUT :
;
; ALGORITHM :
;
; NOTES : created on 1/26/2004
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro regular_hrrd $

    ;input
    ,zbig $			;common extended z-grid
    ,z $			;raw z in selected extended altitude range
    ,u $			;raw u in selected extended altitude range
    ,flag $			;enough data available/not available

    ;output
    ,ugrid $			;u interpolated to regular grid
    ,zgrid			;corresponding regular z-grid

nodata=-999.

;do not have enough valid data
if flag eq 1 then begin
    ugrid=nodata
    zgrid=nodata
    return
endif

;--> zgrid, the extended z-grid (m) specific to the given variable
i0=(where(zbig ge min(z)))(0)
i1=(where(zbig ge max(z)))(0)-1
zgrid=zbig(i0:i1)

; interpolate to the extended z-grid
ugrid=spline(z,u,zgrid)

return
end
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; PURPOSE : map [u,v,t,p][p,b] in zgrid[[u,v,t,p] to the desired zkm
;
; INPUT :
;
; OUTPUT :
;
; ALGORITHM :
;
; NOTES : create on 1/26/2004
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro map_hrrd $

            ;input
            ,flag $	;0: enough valid data; 1: not enough
            ,zgrid $	;extended z-grid (m) specific to the given variable
            ,zm $	;common z-grid (desired)

            ;input/output
            ,up $	;perturbation
            ,ub		;background

nz=n_elements(zm)
;not enough data
if flag eq 1 then begin
    up=replicate(-999.,nz)
    ub=replicate(-999.,nz)
    return
endif else begin
    i0=(where(zgrid ge min(zm)))(0)
    i1=(where(zgrid ge max(zm)))(0)-1
    up=up(i0:i1)
    ub=ub(i0:i1)
endelse

return
end

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; PURPOSE : test and plot the perturbation/background for one hrrd sounding
;
; INPUT :
;
; OUTPUT :
;
; ALGORITHM :
;
; NOTES : created on 1/26/2004
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro test_hrrd_perturb,z,u,z2,u2,zgrid,ugrid,zkm,ub,up,flag,m_z,m_u,z0p,z1p $
                     ,fit=fit $			;if set, test the interpolation
                     ,perturb=perturb $		;if set, test the perturbation
                     ,id=id 			;if set, plot the id

if not keyword_set(id) then id=''
ava=where(z ne m_z and u ne m_u,nava)
if nava gt 0 then begin
    if keyword_set(fit) then begin
        loadct,0
        plot,u(ava),z(ava)/1000.,yran=[z0p/1000.,z1p/1000.],xst=1,yst=1,thick=4
        if flag eq 0 then begin
            oplot,u2,z2/1000.,linestyle=1,thick=6
            loadct,40
            oplot,u2,z2/1000.,thick=1,color=240
            loadct,34
            oplot,ugrid,zgrid/1000.,linestyle=2,thick=2,color=74
            loadct,39
            oplot,ub,zkm,linestyle=2,thick=2,color=120
        endif
    endif
    if keyword_set(perturb) and flag eq 0 then begin
        loadct,0
        plot,up,zkm,xst=1,yst=1,thick=4,title=id
    endif
endif

return
end

function digital_smooth,raw_data0,flow,fhigh
;  a low-pass filter is applied with flow=0,fhigh=0.1,nterm=20

   n=n_elements(raw_data0)
   raw_data=[replicate(raw_data0(0),10),raw_data0,replicate(raw_data0(n-1),10)]
   sz = size(raw_data)
   dim = sz(1)
   nterm = 2*n_elements(raw_data0)
   data_in = fltarr(dim+2*nterm)
   data_in(0:nterm-1) = raw_data(0)
   data_in(nterm+dim:dim+2*nterm-1) = raw_data(n_elements(raw_data)-1)
   data_in(nterm:nterm+dim-1) = raw_data
   a = 50
   coeff = digital_filter(double(flow),double(fhigh),double(a),nterm)
;  coeff = digital_filter((flow),(fhigh),(a),nterm)
   data_out = convol(double(data_in),double(coeff))
;  data_out = convol((data_in),(coeff))
   ;as well as the zero padding elements, the end 5 points are discarded
   smooth_data = float(data_out(nterm+10:nterm+dim-1-10))
;  smooth_data = float(data_out(nterm:nterm+dim-1))
   ;plot,raw_data(5:dim-6)
   ;plot,smooth_data
   ;stop
   return,smooth_data
END

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; PURPOSE : analyze one hrrd
;
; INPUT : fname                  ;name of single radiosonde sounding file
;         z0                     ;bottom z (m)
;         z1                     ;top z (m)
;         buffer                 ;buffer*dz = extended range, e.g., 34
;         dz                     ;vertical resolution (m)
;         lat                    ;latitude (deg)
;         outname		 ;file name of the output
;
; OUTPUT : create a file of name outname which contains the
;
; ALGORITHM : [1] read raw data
;             [2] select the right raw data
;             [3] interpolate the raw data into regular grid
;             [4] get the perturbations and background fields
;             [5] do gw analysis
;
; EXAMPLES : gw_eclipse_complete,'../data/eclipse/T36_0230_121520_Artemis_Rerun_CLEAN.txt',$
;		2000.,8900.,3,30.,-39.2,gw=gw,npoly=2
;            3 is buffer;30.is dz,45.is lat.
;	     the major results are stored in the structure "gw"
;
; HISORY: modified from a1.pro. Changed the reader routine to fit the format of 2020 eclipse data format in 2022.
;	modified on 03/04/2024 to largely remove redundant subroutines by J. Gong.
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

pro gw_eclipse_complete $

               ;all are input
               ,fname $			;name of hrrd
               ,z0 $			;bottom z (m)
               ,z1 $			;top z (m)
               ,buffer $		;buffer*dz = extended range, e.g., 34
               ,dz $			;vertical resolution (m)
               ,lat $			;latitude (deg)
               ,cliptop=cliptop $	;if set, do not extend the top
               ,clipbot=clipbot $	;if set, do not extend the bottom
               ,draw=draw $		;if set, plot the perturbations, etc.
					;obsolete, use uplot etc
               ,uplot=uplot $		;plot the perturbations, etc. for u
               ,vplot=vplot $		;plot the perturbations, etc. for v
               ,tplot=tplot $		;plot the perturbations, etc. for t
               ,pplot=pplot $		;plot the perturbations, etc. for p
               ,nogw=nogw $		;if set, do not analyze gw
               ,npoly=npoly $		;order of polynomial fit
               ,flow=flow $ 		;lower limit of the high-pass filter
               ,fhigh=fhigh $ 		;upper limit of the low-pass filter
               ,id=id $ 		;id+analysis method of the sounding
               ,gw=gw $ 		;id+analysis method of the sounding
               ,notes=notes  		;notes of code

if ~ keyword_set(id) then id=''
if ~ keyword_set(notes) then notes=''

;[A] read in raw data and setting up some universal parameters
read_eclipse,fname,data,nrec,missing,code

z=data.z(0:nrec-1)
u=data.u(0:nrec-1)
v=data.v(0:nrec-1)
ar=data.rs(0:nrec-1)
p=data.p(0:nrec-1)
t=data.t(0:nrec-1)
lat=data.lat(0:nrec-1)
lon=data.lon(0:nrec-1)
m_z=missing.z
m_u=missing.u
m_v=missing.v
m_ar=missing.rs
m_p=missing.p
m_t=missing.t
m_lat=missing.lat
m_lon=missing.lon

if ~ keyword_set(clipbot) then z0p=z0-buffer*dz else z0p=z0-5*dz
if ~ keyword_set(cliptop) then z1p=z1+buffer*dz else z1p=z1+5*dz
zm=make_array3(z0,z1,dz)		;z-grid (m)
zkm=zm/1000.				;z-grid (km)
zbig=make_array3(z0p,z1p,dz)		;the common extended z-grid (m)

;[B] select the approximate data
;--> flag[u,v,t,p]	:		enough data available/not available
;    [u,v,t,p]2		:		raw data in the extended z-range
;    z2[u,v,t,p]	:		the corresponding z

inputflag=0
check_hrrd_gap,z,u,m_z,m_u,z0,z1,z0p,z1p,'U',flagu,z2u,u2
check_hrrd_gap,z,v,m_z,m_v,z0,z1,z0p,z1p,'V',flagv,z2v,v2
check_hrrd_gap,z,ar,m_z,m_ar,z0,z1,z0p,z1p,'AR',flagar,z2ar,ar2
check_hrrd_gap,z,t,m_z,m_t,z0,z1,z0p,z1p,'T',flagt,z2t,t2
check_hrrd_gap,z,p,m_z,m_p,z0,z1,z0p,z1p,'P',flagp,z2p,p2


if flagu EQ 1 or flagv EQ 1 or flagar EQ 1 or flagt EQ 1 $
	or flagp EQ 1 then begin
    inputflag=1
    goto,output_round
endif
check_hrrd_gap,z,lat,m_z,m_lat,z0,z1,z0p,z1p,'Lat',flaglat,z2lat,lat2
check_hrrd_gap,z,lon,m_z,m_lon,z0,z1,z0p,z1p,'Lon',flaglon,z2lon,lon2

;[C] interpolate the data into regular grid
;--> [u,v,t,p]grid	:		raw data interpolated to regular grid
;    zgrid[u,v,t,p]	:		the corresponding z-grid

regular_hrrd,zbig,z2u,u2,flagu,ugrid,zgridu
regular_hrrd,zbig,z2v,v2,flagv,vgrid,zgridv
regular_hrrd,zbig,z2ar,ar2,flagar,argrid,zgridar
regular_hrrd,zbig,z2t,t2,flagt,tgrid,zgridt
regular_hrrd,zbig,z2p,p2,flagp,pgrid,zgridp
regular_hrrd,zbig,z2lat,lat2,flaglat,latgrid,zgridlat
regular_hrrd,zbig,z2lon,lon2,flaglon,longrid,zgridlon

;[D] cal. the perturbations at zgrid[u,v,t,p]
;--> [u,v,t,p][p,b]
perturb_hrrd,ugrid,flagu,npoly=npoly,flow=flow,fhigh=fhigh,up,ub
perturb_hrrd,vgrid,flagv,npoly=npoly,flow=flow,fhigh=fhigh,vp,vb
perturb_hrrd,argrid,flagar,npoly=npoly,flow=flow,fhigh=fhigh,arp,arb
perturb_hrrd,tgrid,flagt,npoly=npoly,flow=flow,fhigh=fhigh,tp,tb
perturb_hrrd,pgrid,flagp,npoly=npoly,flow=flow,fhigh=fhigh,pp,pb
perturb_hrrd,latgrid,flaglat,npoly=npoly,flow=flow,fhigh=fhigh,latp,latb
perturb_hrrd,longrid,flaglon,npoly=npoly,flow=flow,fhigh=fhigh,lonp,lonb


;[E] map [u,v,t,p][p,b] in zgrid[[u,v,t,p] to the desired zm/zkm
map_hrrd,flagu,zgridu,zm,up,ub
map_hrrd,flagv,zgridv,zm,vp,vb
map_hrrd,flagar,zgridar,zm,arp,arb
map_hrrd,flagt,zgridt,zm,tp,tb
map_hrrd,flagp,zgridp,zm,pp,pb
map_hrrd,flaglat,zgridlat,zm,latp,latb
map_hrrd,flaglon,zgridlon,zm,lonp,lonb

;[F] test and plot the perturbation/background
if keyword_set(draw) then $
    test_hrrd_perturb,z,u,z2u,u2,zgridu,ugrid,zkm,ub,up,flagu,m_z,m_u,z0p,z1p $
                     ,/perturb,id=id+' U'
if keyword_set(uplot) then $
    test_hrrd_perturb,z,u,z2u,u2,zgridu,ugrid,zkm,ub,up,flagu,m_z,m_u,z0p,z1p $
                     ,/perturb,id=id+' U'
if keyword_set(vplot) then $
    test_hrrd_perturb,z,v,z2v,v2,zgridv,vgrid,zkm,vb,vp,flagv,m_z,m_v,z0p,z1p $
                     ,/perturb,id=id+' V'
if keyword_set(vplot) then $
    test_hrrd_perturb,z,v,z2ar,ar2,zgridar,argrid,zkm,arb,arp,flagar,m_z,m_ar,$
    z0p,z1p,/perturb,id=id+' AR'
if keyword_set(wplot) then $
    test_hrrd_perturb,z,t,z2t,t2,zgridt,tgrid,zkm,tb,tp,flagt,m_z,m_t,z0p,z1p $
                     ,/perturb,id=id+' T'
if keyword_set(pplot) then $
    test_hrrd_perturb,z,p,z2p,p2,zgridp,pgrid,zkm,pb,pp,flagp,m_z,m_p,z0p,z1p $
                     ,/perturb,id=id+' P'

;[G] convert the unit of T
if flagt eq 0 then tb=tb+273.16		;C-->K

output_round:
;[H] do the gravity wave analysis
if ~ keyword_set(nogw) and inputflag EQ 0 then begin
    input={up:up,vp:vp,arp:arp,tp:tp,um:ub,vm:vb,arm:arb,$
	    tm:tb,pm:pb,lat:latb,lon:lonb,z:zm*1.e-3,dz:dz*1.e-3,ipw:0,iw:0,id:0}
    gw=gw_analysis_struct(input)
endif
if keyword_set(nogw) or inputflag NE 0 then begin
    gw={ke:-999.,outputflag:1}
endif

return
end
