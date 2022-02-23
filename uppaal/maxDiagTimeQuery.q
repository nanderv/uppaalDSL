//This file was generated from (Academic) UPPAAL 4.1.25-5 (rev. 643E9477AA51E17F), April 2021

/*

*/
Pr[<=50000; 70000] ( <> ( GotCpapForeverTimer.total>0 ) )\

/*

*/
Pr[<=50000; 70000] ( <> ( GotCpapForeverTimer.total<=diagnosisMaximumTime && GotCpapForeverTimer.total > 0 ) )\

/*

*/
E[<=50000; 70000] (max:GotCpapForeverTimer.total)\


