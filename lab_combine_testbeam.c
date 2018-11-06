#include <iostream>
#include <fstream>
using namespace std;

void lab_combine_testbeam(TString root_filename, TString lab_filename)
{

	//opening file
	TFile f1(root_filename, "UPDATE");
	TTree *pulse = (TTree*)f1.Get("pulse");
	int tree_entries = pulse->GetEntries();
	//preparing out branches
    float lab_timestamp,sm1_v,sm1_i,sm2_v,sm2_i,sm3_v,sm3_i,sm4_v,sm4_i,sm5_v,sm5_i,photek_v,photek_i,lvpsu_ch1_v,lvpsu_ch1_i,lvpsu_ch2_v,lvpsu_ch2_i,lvpsu_ch3_v,lvpsu_ch3_i,ch_16_res,ch_17_res,ch_18_res,ch_19_res,ch_20_res,labview_warning_bool,del_t_labview;
    int i = 0;

	TBranch * b_lab_timestamp = pulse->Branch("lab_timestamp",&lab_timestamp,"lab_timestamp/F");
	pulse->SetBranchAddress("lab_timestamp",&lab_timestamp,&b_lab_timestamp);

	TBranch * b_sm1_v = pulse->Branch("sm1_v",&sm1_v,"sm1_v/F");
	pulse->SetBranchAddress("sm1_v",&sm1_v,&b_sm1_v);

	TBranch * b_sm1_i = pulse->Branch("sm1_i",&sm1_i,"sm1_i/F");
	pulse->SetBranchAddress("sm1_i",&sm1_i,&b_sm1_i);

	TBranch * b_sm2_v = pulse->Branch("sm2_v",&sm2_v,"sm2_v/F");
	pulse->SetBranchAddress("sm2_v",&sm2_v,&b_sm2_v);

	TBranch * b_sm2_i = pulse->Branch("sm2_i",&sm2_i,"sm2_i/F");
	pulse->SetBranchAddress("sm2_i",&sm2_i,&b_sm2_i);

	TBranch * b_sm3_v = pulse->Branch("sm3_v",&sm3_v,"sm3_v/F");
	pulse->SetBranchAddress("sm3_v",&sm3_v,&b_sm3_v);

	TBranch * b_sm3_i = pulse->Branch("sm3_i",&sm3_i,"sm3_i/F");
	pulse->SetBranchAddress("sm3_i",&sm3_i,&b_sm3_i);

	TBranch * b_sm4_v = pulse->Branch("sm4_v",&sm4_v,"sm4_v/F");
	pulse->SetBranchAddress("sm4_v",&sm4_v,&b_sm4_v);

	TBranch * b_sm4_i = pulse->Branch("sm4_i",&sm4_i,"sm4_i/F");
	pulse->SetBranchAddress("sm4_i",&sm4_i,&b_sm4_i);

	TBranch * b_sm5_v = pulse->Branch("sm5_v",&sm5_v,"sm5_v/F");
	pulse->SetBranchAddress("sm5_v",&sm5_v,&b_sm5_v);

	TBranch * b_sm5_i = pulse->Branch("sm5_i",&sm5_i,"sm5_i/F");
	pulse->SetBranchAddress("sm5_i",&sm5_i,&b_sm5_i);

	TBranch * b_photek_v = pulse->Branch("photek_v",&photek_v,"photek_v/F");
	pulse->SetBranchAddress("photek_v",&photek_v,&b_photek_v);

	TBranch * b_photek_i = pulse->Branch("photek_i",&photek_i,"photek_i/F");
	pulse->SetBranchAddress("photek_i",&photek_i,&b_photek_i);

	TBranch * b_lvpsu_ch1_v = pulse->Branch("lvpsu_ch1_v",&lvpsu_ch1_v,"lvpsu_ch1_v/F");
	pulse->SetBranchAddress("lvpsu_ch1_v",&lvpsu_ch1_v,&b_lvpsu_ch1_v);

	TBranch * b_lvpsu_ch1_i = pulse->Branch("lvpsu_ch1_i",&lvpsu_ch1_i,"lvpsu_ch1_i/F");
	pulse->SetBranchAddress("lvpsu_ch1_i",&lvpsu_ch1_i,&b_lvpsu_ch1_i);

	TBranch * b_lvpsu_ch2_v = pulse->Branch("lvpsu_ch2_v",&lvpsu_ch2_v,"lvpsu_ch2_v/F");
	pulse->SetBranchAddress("lvpsu_ch2_v",&lvpsu_ch2_v,&b_lvpsu_ch2_v);

	TBranch * b_lvpsu_ch2_i = pulse->Branch("lvpsu_ch2_i",&lvpsu_ch2_i,"lvpsu_ch2_i/F");
	pulse->SetBranchAddress("lvpsu_ch2_i",&lvpsu_ch2_i,&b_lvpsu_ch2_i);

	TBranch * b_lvpsu_ch3_v = pulse->Branch("lvpsu_ch3_v",&lvpsu_ch3_v,"lvpsu_ch3_v/F");
	pulse->SetBranchAddress("lvpsu_ch3_v",&lvpsu_ch3_v,&b_lvpsu_ch3_v);

	TBranch * b_lvpsu_ch3_i = pulse->Branch("lvpsu_ch3_i",&lvpsu_ch3_i,"lvpsu_ch3_i/F");
	pulse->SetBranchAddress("lvpsu_ch3_i",&lvpsu_ch3_i,&b_lvpsu_ch3_i);

	TBranch * b_ch_16_res = pulse->Branch("ch_16_res",&ch_16_res,"ch_16_res/F");
	pulse->SetBranchAddress("ch_16_res",&ch_16_res,&b_ch_16_res);


	TBranch * b_ch_17_res = pulse->Branch("ch_17_res",&ch_17_res,"ch_17_res/F");
	pulse->SetBranchAddress("ch_17_res",&ch_17_res,&b_ch_17_res);


	TBranch * b_ch_18_res = pulse->Branch("ch_18_res",&ch_18_res,"ch_18_res/F");
	pulse->SetBranchAddress("ch_18_res",&ch_18_res,&b_ch_18_res);


	TBranch * b_ch_19_res = pulse->Branch("ch_19_res",&ch_19_res,"ch_19_res/F");
	pulse->SetBranchAddress("ch_19_res",&ch_19_res,&b_ch_19_res);


	TBranch * b_ch_20_res = pulse->Branch("ch_20_res",&ch_20_res,"ch_20_res/F");
	pulse->SetBranchAddress("ch_20_res",&ch_20_res,&b_ch_20_res);


	TBranch * b_labview_warning_bool = pulse->Branch("labview_warning_bool",&labview_warning_bool,"labview_warning_bool/F");
	pulse->SetBranchAddress("labview_warning_bool",&labview_warning_bool,&b_labview_warning_bool);

	TBranch * b_del_t_labview = pulse->Branch("del_t_labview",&del_t_labview,"del_t_labview/F");
	pulse->SetBranchAddress("del_t_labview",&del_t_labview,&b_del_t_labview);

	//read text file
    ifstream infile;
    infile.open(lab_filename); 

    while(infile >> lab_timestamp >> sm1_v >> sm1_i >> sm2_v >> sm2_i >> sm3_v >> sm3_i >> sm4_v >> sm4_i >> sm5_v >> sm5_i >> photek_v >> photek_i >> lvpsu_ch1_v >> lvpsu_ch1_i >> lvpsu_ch2_v >> lvpsu_ch2_i >> lvpsu_ch3_v >> lvpsu_ch3_i >> ch_16_res >> ch_17_res >> ch_18_res >> ch_19_res >> ch_20_res >> labview_warning_bool >> del_t_labview){
    	b_lab_timestamp->Fill();
	    b_sm1_v->Fill();
	    b_sm2_v->Fill();
	    b_sm3_v->Fill();
	    b_sm4_v->Fill();
	    b_sm5_v->Fill();
	    b_sm1_i->Fill();
	    b_sm2_i->Fill();
	    b_sm3_i->Fill();
	    b_sm4_i->Fill();
	    b_sm5_i->Fill();
	    b_photek_v->Fill();
	    b_photek_i->Fill();
	    b_lvpsu_ch1_v->Fill();
	    b_lvpsu_ch1_i->Fill();
	    b_lvpsu_ch2_v->Fill();
	    b_lvpsu_ch2_i->Fill();
	    b_lvpsu_ch3_v->Fill();
	    b_lvpsu_ch3_i->Fill();
	    b_ch_16_res->Fill();
	    b_ch_17_res->Fill();
	    b_ch_18_res->Fill();
	    b_ch_19_res->Fill();
	    b_ch_20_res->Fill();
	    b_labview_warning_bool->Fill();
	    b_del_t_labview->Fill();
	    i = i + 1;
	}
	std::cout << "Entries in the tree: " << tree_entries << endl; 
	std::cout << "Entries in the labview file: " << i << endl; 
	pulse->Write();
    f1.Close();
}
