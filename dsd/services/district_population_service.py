from dsd.models.district_population import DistrictPopulation


def sync():
    all_remote_district_populations = DistrictPopulation.objects.all()
    all_local_district_populations = [DistrictPopulation(**remote_dis_popu.__dict__)
                                      for remote_dis_popu in all_remote_district_populations]

    save_district_populations(all_local_district_populations)


def save_district_populations(populations):
    for population in populations:
        filter_result = DistrictPopulation.objects.filter(district=population.district)
        if not filter_result.count():
            population.save()
            continue

        if is_updated(population):
            existing_district_population = DistrictPopulation.objects.get(district=population.district)
            existing_district_population.population_size = population.population_size

            existing_district_population.year = population.year
            existing_district_population.date_created = population.date_created
            existing_district_population.district = population.district
            existing_district_population.save()


def is_updated(remote_population):
    district_population = DistrictPopulation.objects.get(district=remote_population.district)
    return district_population.population_size != remote_population.population_size or \
        district_population.year != remote_population.year or \
        district_population.date_created != remote_population.date_created
