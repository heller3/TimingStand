using namespace::std;
void plot_invest(TString run_number, int isvme, TString channel_number)
{
  if (isvme == 1)
		{
		  TFile f1("/home/daq/Data/CMSTiming/test" + run_number + ".root", "READ");
		  TTree *pulse = (TTree*)f1.Get("pulse");
		  auto c1 = new TCanvas("c1","c1",2000,1400);
		  c1->Divide(1,3,0,0);
		  TPad *pad(NULL);	
		  pad = static_cast<TPad *>(c1->cd(1));	
		  //pad->SetLeftMargin(0.2);	
		  pad->SetBottomMargin(0.14);
		  pad->SetTopMargin(0.1);
		  pad->SetRightMargin(0.1);
		  pulse->Draw("channel[" + channel_number + "]:time[0]");
		  pad = static_cast<TPad *>(c1->cd(2));	
		  //pad->SetLeftMargin(0.2);	
		  pad->SetBottomMargin(0.14);
		  pad->SetTopMargin(0.1);
		  pad->SetRightMargin(0.1);
		  pulse->Draw("amp[" + channel_number + "]");
		  pad = static_cast<TPad *>(c1->cd(3));	
		  //pad->SetLeftMargin(0.2);	
		  pad->SetBottomMargin(0.14);
		  pad->SetTopMargin(0.1);
		  pad->SetRightMargin(0.1);
		  pulse->Draw("LP1_30[" + channel_number +  "]-LP1_30[8]","LP1_30[" + channel_number + "]>0");
		}
  else if (isvme == 0)
		{
		  TFile f1("/home/daq/Data/NetScopeTiming/test" + run_number + ".root", "READ");
		  TTree *pulse = (TTree*)f1.Get("pulse");
		  auto c1 = new TCanvas("c1","c1",2000,1400);
		  c1->Divide(1,3,0,0);
		  TPad *pad(NULL);	
		  pad = static_cast<TPad *>(c1->cd(1));	
		  //pad->SetLeftMargin(0.2);	
		  pad->SetBottomMargin(0.14);
		  pad->SetTopMargin(0.1);
		  pad->SetRightMargin(0.1);
		  c1->cd(1);
		  pulse->Draw("channel[" + channel_number + "]:time[0]");	
		  pad = static_cast<TPad *>(c1->cd(2));	
		  //pad->SetLeftMargin(0.2);	
		  pad->SetBottomMargin(0.14);
		  pad->SetTopMargin(0.1);
		  pad->SetRightMargin(0.1);
		  pulse->Draw("amp[" + channel_number + "]");	
		  pad = static_cast<TPad *>(c1->cd(3));	
		  //pad->SetLeftMargin(0.2);	
		  pad->SetBottomMargin(0.14);
		  pad->SetTopMargin(0.1);
		  pad->SetRightMargin(0.1);
		  pulse->Draw("LP1_30[" + channel_number +  "]-LP1_30[0]","LP1_30[" + channel_number + "]>0");
		}
}
