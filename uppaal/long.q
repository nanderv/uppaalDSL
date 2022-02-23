//This file was generated from (Academic) UPPAAL 4.1.25-5 (rev. 643E9477AA51E17F), April 2021

/*
For the analysis software: what is the prevalence of OSA
*/
Pr[<=50000; 350000] ( <> ( has_osa ) )\


/*
True positive diagnoses
*/
Pr[<=50000; 350000] (<> ( Dhas_osa && has_osa ))\


/*
False negative diagnoses
*/
Pr[<=50000; 350000] ( <> ( has_osa && Dno_osa ) )\


/*
True negative diagnoses
*/
Pr[<=50000; 350000] ( <> ( no_osa && Dno_osa ) )\


/*
False positive diagnoses  [4]
*/
Pr[<=50000; 350000] ( <> ( no_osa && Dhas_osa ) )\


/*
Total cost of diagnosis [5]
*/
E[<=50000; 350000] (max:TOTAL_COST)\


/*
Time to diagnosis [6]
*/
E[<=50000; 350000] (max:DiagnosisTimer.total)\


/*
Percentage of patients receiving treatment [7]
*/
Pr[<=50000; 350000] ( <> ( TreatmentTimer.total>0 ) )\


/*

*/
Pr[<=50000; 350000] ( <> ( GotCpapForeverTimer.total>0 ) )\


/*

*/
E[<=50000; 350000] (max:GotCpapForeverTimer.total)\


/*

*/
Pr[<=50000; 350000] ( <> ( otherTreatment>0 ) )\


/*

*/
Pr[<=50000; 350000] ( <> ( startFinalTreatment>0 ) )\

