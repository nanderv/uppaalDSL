//This file was generated from (Academic) UPPAAL 4.1.25-5 (rev. 643E9477AA51E17F), April 2021

/*

*/
Pr[<=50000; 500000] ( <> ( DiagnosisTimer.total>0 ) )\

/*

*/
Pr[<=50000; 500000] ( <> ( DiagnosisTimer.total<=diagnosisMaximumTime && DiagnosisTimer.total > 0 ) )\

/*

*/
Pr[<=50000; 500000] ( <> ( DiagnosisTimer.total<=diagnosisMaximumTime && DiagnosisTimer.total > 0  && ( ( Dhas_osa && has_osa ) || ( no_osa && Dno_osa ) ) ))