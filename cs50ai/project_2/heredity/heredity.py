import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_prob = 1

    for person in people:
        father = people[person]["father"]
        if father in one_gene:
            f_ng = 1
        elif father in two_genes:
            f_ng = 2
        else:
            f_ng = 0

        mother = people[person]["mother"]
        if mother in one_gene:
            m_ng = 1
        elif mother in two_genes:
            m_ng = 2
        else:
            m_ng = 0

        if person in one_gene:
            p_ng = 1
        elif person in two_genes:
            p_ng = 2
        else:
            p_ng = 0

        if person in have_trait:
            person_has_trait = True
        else:
            person_has_trait = False        

        if mother == father == None:

            combined_prob = PROBS["gene"][p_ng] * PROBS["trait"][p_ng][person_has_trait]
            joint_prob *=  combined_prob
        else:
            # 2 -> 1.0 - 0.01 = 0.99
            # 1 -> 0.5(1 - 0.01) + 0.5(0 + 0.01) = 0.50 -- it's equally likely that we mutate the non target gene into a target gene and vice versa
            # 0 -> abs(0.0 - 0.01) = 0.01
            # Abstract version: (ng)/2 * (1-0.01) + (2 - ng)/2 * (0 + 0.01) = prob_pass_on
            P_h = lambda ng: (ng/2)*(1-PROBS["mutation"]) + ((2 - ng)/2)*(0 + PROBS["mutation"])

            if person in two_genes:
                
                child_heredity = P_h(m_ng) * P_h(f_ng) * PROBS["trait"][2][person_has_trait]
            elif person in one_gene:
                child_heredity = (P_h(m_ng) * (1-P_h(f_ng)) + P_h(f_ng) * (1-P_h(m_ng))) * PROBS["trait"][1][person_has_trait]
            else:
                child_heredity = (1-P_h(f_ng)) * (1-P_h(m_ng)) * PROBS["trait"][0][person_has_trait]
            joint_prob *= child_heredity
    
    return joint_prob


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        probabilities[person]["trait"][bool(person in have_trait)] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        gene_sum = sum([probabilities[person]["gene"][gene] for gene in range(3)])
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] = probabilities[person]["gene"][gene] / gene_sum

        trait_sum = sum([probabilities[person]["trait"][i] for i in probabilities[person]["trait"]])
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] = probabilities[person]["trait"][trait] / trait_sum



if __name__ == "__main__":
    main()

"""
from heredity import *
people = {
   'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
   'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
   'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}
joint_probability(people, {"Harry"}, {"James"}, {"James"})
"""