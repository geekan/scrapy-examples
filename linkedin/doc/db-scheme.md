Mongodb Scheme(**draft**)

---

**PersonProfile**

	PersonProfile
	{
		linkedin_id:'id',
		locality:'beijing',
		industry:'Research',
		summary:'I am a professor…',
		
		skills:
				[
					'data mining',
					'machine learning'
				],
				
		specilities:
				[
					'data mining',
				],
				
		interests:
				[
					'data mining',
					'machine learning'
				],
				
		groups:
				{
					'member',
					'affiliation':
								[
									'kdd 2012'
								]
				}
				
		honors:
				[
					'first prize',
				],
		
		education:
				[
					{
						school_name: 'a',
						period: '1991-2012',
						desc:'topic model'
					},
				],
				
		experience:
				[
					{
						title:'associate professor',
						organization:'tsinghua',
						period:'1999-2000',
						description:'research about data mining',
					},
				],
				
		also_view:
				[
					{
						'linkedin_id':'asd',
						'url':'http',
					}
				],
		
	}